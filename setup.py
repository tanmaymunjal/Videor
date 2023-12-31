import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type("")
    with io.open(filename, mode="r", encoding="utf-8") as fd:
        return re.sub(text_type(r":[a-z]+:`~?(.*?)`"), text_type(r"``\1``"), fd.read())


with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="Videor",
    version="0.0.1",
    url="https://github.com/tanmaymunjal/Videor",
    license="MIT License",
    author="Tanmay Munjal",
    author_email="tanmaymunjal64@gmail.com",
    description="Python API under development for Video Transcoding",
    long_description=read("README.md"),
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=required,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Multimedia :: Video" "Programming Language :: Python",
    ],
)
