import codecs
import os

from setuptools import find_packages, setup

# Basic information
NAME = "torchmm"
DESCRIPTION = "PyTorch DataLoader and Abstraction for multi-modal data."
VERSION = "0.0.2 alpha"
AUTHOR = "Abdul Waheed, Ganeshan Malhotra"
EMAIL = "abdulwaheed1513@gmail.com"
LICENSE = "MIT"
REPOSITORY = "https://github.com/pytorch-duo/torchmm"
PACKAGE = "torchmm"
with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

# Define the keywords
KEYWORDS = ["machine learning","deep learning", "computer vision", "natural language processing", "pytorch"]

# Define the classifiers
# See https://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Topic :: Software Development",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
]

# Important Paths
PROJECT = os.path.abspath(os.path.dirname(__file__))
REQUIRE_PATH = "requirements.txt"
VERSION_PATH = os.path.join(PACKAGE, "version.py")
PKG_DESCRIBE = "README.md"

# Directories to ignore in find_packages
EXCLUDES = ()


# helper functions
def read(*parts):
    """
    returns contents of file
    """
    with codecs.open(os.path.join(PROJECT, *parts), "rb", "utf-8") as file:
        return file.read()


def get_requires(path=REQUIRE_PATH):
    """
    generates requirements from file path given as REQUIRE_PATH
    """
    for line in read(path).splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            yield line


# Define the configuration
CONFIG = {
    "name": NAME,
    "version": VERSION,
    "description": DESCRIPTION,
    "long_description": LONG_DESCRIPTION,
    "long_description_content_type": "text/markdown",
    "classifiers": CLASSIFIERS,
    "keywords": KEYWORDS,
    "license": LICENSE,
    "author": AUTHOR,
    "author_email": EMAIL,
    "url": REPOSITORY,
    "project_urls": {"Source": REPOSITORY},
    "packages": find_packages(where=PROJECT, exclude=EXCLUDES),
    "install_requires": list(get_requires()),
    "python_requires": ">=3.5",
}

if __name__ == "__main__":
    setup(**CONFIG)
