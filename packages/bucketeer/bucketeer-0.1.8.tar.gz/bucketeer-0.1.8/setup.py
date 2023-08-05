
import io
import os
import sys

from setuptools import Command, find_packages, setup
from bucketeer.version import version_str

NAME = "bucketeer"
DESCRIPTION = "Tool to automatically provide and trackt the lowest used API keys in rotation."
URL = "https://github.com/ms7m/bucketeer"
EMAIL = "git@ms7m.me"
AUTHOR = "Mustafa Mohamed"
REQUIRES_PYTHON = ">=3.6.0"

REQUIRED_PACKAGES = [
    "loguru"
]

EXTRAS = {
    "redis": ["redis==3.5.3"]
}

setup(
    name=NAME,
    version=version_str,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requies=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests"]),
    install_requires=REQUIRED_PACKAGES,
    extras_require=EXTRAS,
    include_package_data=True,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)