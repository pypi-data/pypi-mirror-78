import configparser
import hashlib
import os
import re
import sys

import setuptools


def publish():
    """
    A Shortcut for building the package and pushing it into PyPI.  This is
    lifted entirely from the requests library.
    """
    os.system("rm -vfr build dist")
    os.system("python setup.py build")
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    sys.exit()


def make_aur():
    """
    Use the existing package to generate a PKGBUILD file for Arch Linux's AUR.

    Note that ``python-magic`` is in fact an Arch packaging of the
    ``file-magic`` Python module, and **not** the ``python-magic`` Python
    module.
    """

    with open("aletheia/__init__.py") as f:
        version = re.sub(
            r".* = \((\d+), (\d+), (\d).*",
            "\\1.\\2.\\3",
            f.read().strip()
        )

    package_path = "dist/aletheia-{}.tar.gz".format(version)
    if not os.path.exists(package_path):
        print(
            "The package doesn't exist yet. You should run setup.py publish "
            "first and then try again."
        )
        sys.exit(1)

    with open(package_path, "rb") as f:
        package_hash = hashlib.sha512(f.read()).hexdigest()

    template = """
        # Maintainer: Daniel Quinn <archlinux at danielquinn dot org>

        pkgname="python-aletheia"
        pkgver=VERSION
        pkgrel=1
        pkgdesc="Fight fake news with cryptography & human nature"
        _name=${pkgname#python-}
        arch=('any')
        url="https://pypi.org/project/aletheia/"
        license=('AGPL3')
        makedepends=('python-setuptools')
        depends=('ffmpeg'
        'perl-image-exiftool'
        'python'
        'python-setuptools'
        'python-cryptography'
        'python-dnspython'
        'python-magic'
        'python-requests'
        'python-termcolor')
        source=("https://files.pythonhosted.org/packages/source/${_name::1}/${_name}/${_name}-${pkgver}.tar.gz")
        sha512sums=('HASH')

        build() {
            cd "${srcdir}/${_name}-${pkgver}"
            python setup.py build
        }

        package() {
            cd "${srcdir}/${_name}-${pkgver}"
            python setup.py install --root="${pkgdir}/" --optimize=1 --skip-build
            install -Dm 644 LICENSE "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
            install -Dm 644 README.rst "${pkgdir}/usr/share/doc/${pkgname}/README"
        }
    """  # NOQA: E501
    sys.stdout.write(template.replace(
        "VERSION",
        version
    ).replace(
        "HASH",
        package_hash
    ).replace(
        "        ",
        ""
    ).strip() + "\n")
    sys.exit()


def get_requirements():
    """
    Alpine is problematic in how it doesn't play nice with file-magic -- a
    module that appears to be the standard for most other Linux distros.  As a
    work-around for this, we swap out file-magic for python-magic in the Alpine
    case.
    """

    config = configparser.ConfigParser()
    config.read("setup.cfg")
    requirements = config["options"]["install_requires"].split()

    os_id = None
    try:
        with open("/etc/os-release") as f:
            os_id = [_ for _ in f.readlines() if _.startswith("ID=")][0] \
                .strip() \
                .replace("ID=", "")
    except (FileNotFoundError, OSError, IndexError):
        pass

    if os_id == "alpine":
        requirements[1] = "python-magic>=0.4.15"

    return requirements


# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

if sys.argv[-1] == "publish":
    publish()
elif sys.argv[-1] == "make-aur":
    make_aur()

setuptools.setup(install_requires=get_requirements())
