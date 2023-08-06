#!/usr/bin/env python3
# Copyright (c) 2020 Collabora, Ltd.
#
# SPDX-License-Identifier: Apache-2.0
"""Setup."""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ballparker",
    version="1.0.1",
    author="Ryan A. Pavlik",
    author_email="ryan.pavlik@collabora.com",
    description="A tool for structuring and creating ballpark estimates",
    license="Apache-2.0 AND CC0-1.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ryanpavlik/ballparker",
    project_urls={
        "Source Code and Issue Tracker":
            "https://gitlab.com/ryanpavlik/ballparker",
        "Documentation": "https://ballparker.readthedocs.io",
    },
    packages=setuptools.find_packages(),
    install_requires=["attrs", "typing"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
