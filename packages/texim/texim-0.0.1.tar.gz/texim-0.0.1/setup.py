#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from setuptools import setup, find_packages

try:
    README = open('README.md').read()
except Exception:
    README = ""

setup(
    name='texim',
    version="0.0.1",
    description='texim',
    author='spenly',
    author_email='i@spenly.com',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/spenly/texim.git",
    packages=find_packages(),
    install_requires=[],
    extras_require={},
    entry_points={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5'
)
