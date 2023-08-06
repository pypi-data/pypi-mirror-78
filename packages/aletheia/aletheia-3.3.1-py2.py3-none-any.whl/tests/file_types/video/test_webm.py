import os
import subprocess

from hashlib import md5
from unittest import mock

from cryptography.exceptions import InvalidSignature
from pytest import mark

from aletheia.exceptions import UnparseableFileError
from aletheia.file_types.video.webm import WebmFile

from ...base import TestCase


class WebmTestCase(TestCase):

    def test_get_raw_data_from_path(self):

        unsigned = os.path.join(self.DATA, "original", "test.webm")
        self.assertEqual(
            md5(WebmFile(unsigned, "").get_raw_data()).hexdigest(),
            "c88e8d6125942f74b7fcd9440d693da7"
        )

        signed = os.path.join(self.DATA, "signed", "test.webm")
        self.assertEqual(
            md5(WebmFile(signed, "").get_raw_data()).hexdigest(),
            "c88e8d6125942f74b7fcd9440d693da7",
            "Modifying the metadata should have no effect on the raw data"
        )

    @mark.ffmpeg_min_version34
    def test_sign_from_path(self):

        path = self.copy_for_work("original", "webm")

        f = WebmFile(path, "")
        f.generate_signature = mock.Mock(return_value="signature")
        f.generate_payload = mock.Mock(return_value="payload")
        f.sign(None, "example.com")

        metadata = subprocess.Popen(
            (
                "ffmpeg",
                "-i", path,
                "-loglevel", "error",
                "-f", "ffmetadata", "-",
            ),
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        ).stdout.read()

        self.assertIn(b"ALETHEIA=payload", metadata)

    def test_verify_from_path_no_signature(self):

        path = self.copy_for_work("original", "webm")

        f = WebmFile(path, "")
        self.assertRaises(UnparseableFileError, f.verify)

    def test_verify_bad_signature(self):
        cache = self.cache_public_key()
        path = self.copy_for_work("bad", "webm")

        f = WebmFile(path, cache)
        self.assertRaises(InvalidSignature, f.verify)

    def test_verify_broken_signature(self):
        cache = self.cache_public_key()
        path = self.copy_for_work("broken", "webm")

        f = WebmFile(path, cache)
        self.assertRaises(InvalidSignature, f.verify)

    def test_verify_future_version(self):
        path = self.copy_for_work("future", "webm")
        self.assertRaises(UnparseableFileError, WebmFile(path, "").verify)

    def test_verify_from_path(self):

        path = self.copy_for_work("signed", "webm")

        f = WebmFile(path, "")
        f.verify_signature = mock.Mock(return_value=True)
        self.assertTrue(f.verify())
