import base64
import logging
import os
import shutil
import tempfile
import unittest

from aletheia.aletheia import Aletheia
from aletheia.exceptions import PrivateKeyNotDefinedError

from .base import EnvironmentVarGuard


class AletheiaTestCase(unittest.TestCase):

    def setUp(self):

        self.env = EnvironmentVarGuard()
        self.scratch = tempfile.mkdtemp(prefix="aletheia-tests-")
        self.env["HOME"] = self.scratch

        os.makedirs(self.env["HOME"], exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.scratch, ignore_errors=True)

    def test___init___defaults(self):

        with self.env:
            aletheia = Aletheia()

        home = "{}/.config/aletheia".format(self.scratch)
        self.assertEqual(
            aletheia.private_key_path, "{}/aletheia.pem".format(home))
        self.assertEqual(
            aletheia.public_key_path, "{}/aletheia.pub".format(home))
        self.assertEqual(
            aletheia.public_key_cache, "{}/public-keys".format(home))

    def test___init___with_values(self):

        with self.env:
            aletheia = Aletheia(
                private_key_path="alpha",
                public_key_path="bravo",
                cache_dir="charlie"
            )

        self.assertEqual(aletheia.private_key_path, "alpha")
        self.assertEqual(aletheia.public_key_path, "bravo")
        self.assertEqual(aletheia.public_key_cache, "charlie")

    def test_generate(self):

        with self.env:
            Aletheia().generate()

        home = os.path.join(self.scratch, ".config", "aletheia")
        self.assertTrue(os.path.exists(os.path.join(home, "aletheia.pem")))
        self.assertTrue(os.path.exists(os.path.join(home, "aletheia.pub")))

        with open(os.path.join(home, "aletheia.pem")) as f:
            self.assertIn("BEGIN", f.read())

        with open(os.path.join(home, "aletheia.pub")) as f:
            self.assertIn("BEGIN", f.read())

    def test_sign_file_doesnt_exist(self):

        with self.env:
            aletheia = Aletheia()

        self.assertRaises(
            FileNotFoundError, aletheia.sign, "/dev/null/nowhere", "")

    def test_verify_file_doesnt_exist(self):

        with self.env:
            aletheia = Aletheia()

        self.assertRaises(
            FileNotFoundError, aletheia.verify, "/dev/null/nowhere")

    def test__get_private_key_in_environment(self):

        private_key_path = os.path.join(
            os.path.dirname(__file__), "data", "keys", "private.pem")
        with open(private_key_path) as f:
            self.env["ALETHEIA_PRIVATE_KEY"] = f.read()

        with self.env:
            self.assertIsNotNone(Aletheia()._get_private_key())

    def test__get_private_key_in_environment_as_base64(self):

        private_key_path = os.path.join(
            os.path.dirname(__file__), "data", "keys", "private.pem")
        with open(private_key_path, "rb") as f:
            self.env["ALETHEIA_PRIVATE_KEY"] = base64.encodebytes(f.read()).decode().replace("\n", "")

        with self.env:
            self.assertIsNotNone(Aletheia()._get_private_key())

    def test__get_private_key_in_environment_as_bad_base64(self):

        private_key_path = os.path.join(
            os.path.dirname(__file__), "data", "keys", "private.pem")
        with open(private_key_path, "rb") as f:
            self.env["ALETHEIA_PRIVATE_KEY"] = base64.encodebytes(f.read()).decode().replace("\n", "").replace("A", "_")

        with self.env:
            with self.assertLogs("aletheia", logging.WARNING) as logger:
                self.assertRaises(PrivateKeyNotDefinedError, Aletheia()._get_private_key)
                self.assertEqual(len(logger.output), 1)
                self.assertIn("can't be understood", logger.output[0])

    def test__get_bad_private_key_in_environment_no_file(self):

        private_key_path = os.path.join(
            os.path.dirname(__file__), "data", "keys", "private.pem")
        with open(private_key_path) as f:
            self.env["ALETHEIA_PRIVATE_KEY"] = f.read().replace(
                "BEGIN RSA PRIVATE KEY",
                "Not a private key"
            )

        with self.env:
            self.assertRaises(
                PrivateKeyNotDefinedError,
                Aletheia()._get_private_key
            )

    def test__get_private_key_in_file(self):

        private_key_path = os.path.join(
            os.path.dirname(__file__), "data", "keys", "private.pem")

        with self.env:
            aletheia = Aletheia(private_key_path=private_key_path)
            self.assertIsNotNone(aletheia._get_private_key())

    def test__get_private_key_doesnt_exist(self):
        with self.env:
            self.assertRaises(
                PrivateKeyNotDefinedError,
                Aletheia()._get_private_key
            )
