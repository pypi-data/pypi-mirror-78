#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import setuptools
from setuptools.command.build_py import build_py


NAME = "ciocore"
DESCRIPTION = "Core functionality for Conductor's client tools"
URL = "https://github.com/AtomicConductor/conductor-core"
EMAIL = "info@conductortech.com"
AUTHOR = "conductor"
REQUIRES_PYTHON = "~=2.7"
REQUIRED = ["pyjwt>=1.4.2",  "requests>=2.10.0"]
HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, 'VERSION')) as version_file:
    VERSION = version_file.read().strip()


class BuildCommand(build_py):
    def run(self):
        build_py.run(self)

        if not self.dry_run:
            with open(os.path.join(self.build_lib, NAME, "VERSION"), "w") as f:
                f.write(VERSION)


setuptools.setup(
    author=AUTHOR,
    author_email=EMAIL,
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python",
        "Topic :: Multimedia :: Graphics :: 3D Rendering",
    ],
    cmdclass={"build_py": BuildCommand},
    description=DESCRIPTION,
    scripts=['bin/conductor'],
    include_package_data=True,
    install_requires=REQUIRED,
    long_description=DESCRIPTION,
    long_description_content_type="text/markdown",
    name=NAME,
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=REQUIRES_PYTHON,
    url=URL,
    version=VERSION,
    zip_safe=False,

)
