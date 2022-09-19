import os
from setuptools import setup, find_packages

with open(
        os.path.join(os.path.dirname(__file__), "requirements/common.txt"), "r"
) as fh:
    requirements = fh.readlines()

NAME = "podfile"
DESCRIPTION = "这是一个python库，可以很好的编辑Podfile文件"
AUTHOR = "zzz"
URL = "https://github.com/zhtut/podfile"
VERSION = None

about = {}

with open("README.md", "r") as fh:
    about["long_description"] = fh.read()

root = os.path.abspath(os.path.dirname(__file__))

if not VERSION:
    with open(os.path.join(root, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION

setup(
    name=NAME,
    version=about["__version__"],
    license="MIT",
    description=DESCRIPTION,
    long_description=about["long_description"],
    long_description_content_type="text/markdown",
    AUTHOR=AUTHOR,
    url=URL,
    keywords=["ios", "python", "cocoapods", "podfile"],
    install_requires=[req for req in requirements],
    packages=find_packages(exclude=("tests",), include=("podfile", "yaml_podfile", "common")),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
)
