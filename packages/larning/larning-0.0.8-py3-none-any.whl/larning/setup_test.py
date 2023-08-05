from larning.testing import name
from larning.setup import PACKAGE_NAME, find_packages


@name(find_packages, 1, globals())
def _():
    assert find_packages()[0] == "larning"


@name(find_packages, 2, globals())
def _():
    assert PACKAGE_NAME == "larning"
