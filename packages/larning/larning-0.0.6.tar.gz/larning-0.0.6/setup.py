#! /usr/bin/env python
from sys import version_info
from re import split
from typing import List
from urllib.request import urlopen
from json import loads
from shutil import rmtree
from os.path import dirname, realpath, join
from setuptools import setup, find_packages

# consts
package_name = find_packages()[0]
with open("README.md", "r") as fh:
    long_description = fh.read()
root_path = dirname(realpath(__file__))
dist_path = join(root_path, "dist")
egg_info_path = join(root_path, package_name + ".egg-info")
build_path = join(root_path, "build")
# funcs
def current_pypi_release() -> str:
    with urlopen("https://pypi.org/pypi/" + package_name + "/json") as url:
        data: dict = loads(url.read().decode())
        releases: dict = data["releases"]
        release_strs = list(releases.keys())
        return release_strs[-1]


def release_to_ints(release: str) -> List[int]:
    return [int(i) for i in split("\.", release)]


def increase_ints(ints: List[int]) -> List[int]:
    ints[-1] += 1
    return ints


def to_release(ints: List[int], splitter: str = ".") -> str:
    ret = ""
    for i, int_ in enumerate(ints):
        if i != 0:
            ret += "."
        ret += str(int_)
    return ret


# ˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇ
release = to_release([0, 0, 0])
install_requires = ["twine", "pydantic", "sphinx", "setuptools", "black", "pytest", "wheel"]
author = "Tasnádi Gábor"
email = "tasi.gabi97@gmail.com"
github_username = "tasigabi97"
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
url = "https://github.com/" + github_username + "/" + package_name
required_interpreter = (3, 6)
if release_to_ints(release) <= release_to_ints(current_pypi_release()):
    release = to_release(increase_ints(release_to_ints(current_pypi_release())))
if version_info[:2] < required_interpreter:
    raise RuntimeError("Python version >= 3.6 required.")
for i in [dist_path, egg_info_path, build_path]:
    try:
        rmtree(i)
    except Exception as e:
        print(e)


setup(
    name=package_name,
    version=release,
    author=author,
    author_email=email,
    description=package_name,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=url,
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
    ],
    install_requires=install_requires,
    keywords=[package_name,],
    license="MIT",
)
