.. include:: globals.rst

************
Installation
************

For installation on the command line of your operating system:

.. code:: bash

    pip install vsutillib

This install all sub packages.

You can also install any individual packages.

.. code:: bash

    pip install vsutillib-files
    pip install vsutillib-log
    pip install vsutillib-macos
    pip install vsutillib-media
    pip install vsutillib-network
    pip install vsutillib-processing
    pip install vsutillib-vsxml

Try to use only one method the packages install under the namespace
**vsutillib**.

The library works on CPython 3.5->3.7

Dependencies
============

Some of the functions and/or classes use the following packages:

    Python packages are installed if pip is used:

        lxml_ - library for processing XML and HTML with Python

        pymediainfo_ - Python MediaInfo wrapper

    MediaInfo_ - unified display of the most relevant technical and
    tag data for video and audio files.  Follow installation instructions
    for the different operating systems.

Installation of MediaInfo is only needed on Linux.  And this is only needed
for everything to work. lxml is use by **vsutillib.vsxml**. pymediainfo_
is use by **vsutillib.media**.

Known Issues
============

.. _pymediainfo: https://pypi.org/project/pymediainfo/
