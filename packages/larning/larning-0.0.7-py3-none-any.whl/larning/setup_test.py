from larning.testing import name
from setuptools import find_packages
from larning.setup import get_package_name


@name(find_packages, 1, globals())
def _():
    assert find_packages()[0] == "larning"


@name(get_package_name, 1, globals())
def _():
    assert get_package_name() == "larning"
