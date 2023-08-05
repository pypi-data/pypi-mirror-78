from os.path import dirname, realpath, join
from setuptools import setup, find_packages


def get_package_name() -> str:
    return find_packages(dirname(realpath("./setup.py")))[0]
