#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""setup file to build python distributions"""

import io
import os
import pathlib
import shutil

from distutils.command.clean import clean
from distutils.command.install import install
from pathlib import Path
from setuptools import setup

from vsutillib import config

ROOT = pathlib.Path(__file__).parent.resolve()


class MyInstall(install):
    """install subclass"""

    # Calls the default run command, then deletes the build area
    # (equivalent to "setup clean --all").
    def run(self):
        print("what to clean {}".format(self.distribution))
        install.run(self)
        c = clean(self.distribution)
        c.all = True
        c.finalize_options()
        c.run()


def removeTmpDirs():
    """
    delete build directory setup was including files from other builds
    """
    p = Path(".")
    eggDirs = [x for x in p.glob("*.egg-info") if x.is_dir()]
    eggDirs.append(Path("build"))

    for d in eggDirs:
        if d.is_dir():
            shutil.rmtree(d)


def readme():
    """get README.rst"""

    try:
        with io.open(os.path.join(ROOT, "README.rst"), encoding="utf-8") as f:
            long_description = "\n" + f.read()
    except FileNotFoundError:
        long_description = config.DESCRIPTION
    return long_description

removeTmpDirs()

setup(
    name=config.NAME,  # Required
    version=config.VERSION,  # Required
    description=config.DESCRIPTION,  # Required
    long_description=readme(),  # Optional
    author=config.AUTHOR,  # Optional
    author_email=config.EMAIL,  # Optional
    url=config.PYPI,
    license="MIT",
    classifiers=[  # Optional
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications :: Qt",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries",
        # Pick your license as you wish
        "License :: OSI Approved :: MIT License",
        # Operating Systems
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: POSIX :: Linux",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3.8",
        # Implementation
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    keywords=config.KEYWORDS,  # Optional
    packages=config.PACKAGES,
    install_requires=config.REQUIRED,
    python_requires=config.PYTHONVERSIONS,
    include_package_data=True,
    project_urls=config.PROJECTURLS,
)

removeTmpDirs()
