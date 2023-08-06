#!/usr/bin/env python
# Copyright 2020 Nokia
# Licensed under the Apache License 2.0.
# SPDX-License-Identifier: Apache-2.0

import os
from setuptools import setup


def slurp(filename):
    """
    Return whole file contents as string. File is searched relative to
    directory where this `setup.py` is located.
    """
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()


setup(
    name                 = "sphinxcontrib.relative-link-corrector",
    version              = "0.0.2",
    packages             = ["sphinxcontrib", "sphinxcontrib.relative-link-corrector"],
    namespace_packages   = ["sphinxcontrib"],
    package_dir          = {'': "src"},
    author               = "Gergely Csatari",
    author_email         = "gergely.csatari@nokia.com",
    license              = "Apache License 2.0",
    url                  = "https://github.com/cntt-n/sphinxcontrib-relative-link-corrector",
    keywords             = ["helpers"],
    install_requires     = ["beautifulsoup4"],
    long_description_content_type = "text/x-rst",
    description          = ("Corrects relative links when generating documents  "
                            "from .md to .html with commonmark"),
    long_description     = slurp("README.rst"),
    classifiers          = ["Programming Language :: Python :: 3",
                            "Development Status :: 4 - Beta",
                            "Topic :: Documentation",
                            "Intended Audience :: Developers",
                            "License :: OSI Approved :: Apache Software License",
                            "Operating System :: POSIX"])

