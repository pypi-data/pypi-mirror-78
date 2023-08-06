#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

"""Setup pycls."""

from setuptools import find_packages, setup


setup(
    name="pycls",
    version="0.1.0",
    description="A codebase for image classification",
    url="https://github.com/facebookresearch/pycls",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        "numpy",
        "opencv-python",
        "simplejson",
        "yacs",
    ],
)
