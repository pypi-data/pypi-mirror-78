# -*- coding: utf-8 -*-

"""Top-level package for Easy Caesar."""

__author__ = "Sam Blumenthal"
__email__ = "sam.sam.42@gmail.com"
# Do not edit this string manually, always use bumpversion
# Details in CONTRIBUTING.md
__version__ = "0.1.0"


def get_module_version():
    return __version__


from .cipher import Cipher  # noqa: F401
