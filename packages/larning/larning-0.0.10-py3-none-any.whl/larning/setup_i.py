from os.path import dirname, realpath, join
from setuptools import setup, find_packages
from urllib.request import urlopen
from json import loads
from re import split
from typing import List
from larning.strings import concatenate_with_separation
from sys import version_info

setup = setup
ROOT = dirname(realpath("./setup.py"))
PACKAGES = find_packages(ROOT)
PACKAGE_NAME = PACKAGES[0]
with open(join(ROOT, "README.md"), "r") as fh:
    LONG_DESCRIPTION = fh.read()


def _get_current_pypi_version() -> str:
    with urlopen("https://pypi.org/pypi/" + PACKAGE_NAME + "/json") as url:
        data: dict = loads(url.read().decode())
        releases: dict = data["releases"]
        release_strs = list(releases.keys())
        return release_strs[-1]


CURRENT_PYPI_VERSION = _get_current_pypi_version()


def require_interpreter_version(major: int, minor: int, micro: int):
    required = (major, minor, micro)
    if version_info[:3] < required:
        raise RuntimeError(f"Python version >= {required} required.")


def get_github_url(username: str):
    return "https://github.com/" + username + "/" + PACKAGE_NAME


def get_version(major: int, minor: int, micro: int):
    def _version_to_ints(release: str) -> List[int]:
        return [int(i) for i in split(r"\.", release)]

    def _increase_ints(ints: List[int]) -> List[int]:
        ints[-1] += 1
        return ints

    def _to_release(ints: List[int]) -> str:
        return concatenate_with_separation(ints, ".")

    version_ints = [major, minor, micro]
    if version_ints <= _version_to_ints(CURRENT_PYPI_VERSION):
        return _to_release(_increase_ints(_version_to_ints(CURRENT_PYPI_VERSION)))
    return _to_release(version_ints)
