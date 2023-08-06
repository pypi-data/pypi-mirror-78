****************************************************
vsutillib: module with utility functions and classes
****************************************************


.. image:: https://img.shields.io/pypi/v/vsutillib.svg
  :target: https://pypi.org/project/vsutillib

.. image:: https://img.shields.io/pypi/pyversions/vsutillib.svg
  :target: https://pypi.org/project/vsutillib


These are a collection of functions and classes that I use on
my applications to made easier to maintain I decided to release
it and install as a dependency of apps like mkvbatchmultiplex.

Description
===========

A range of functions and classes with a variety of uses for
example:

    - functions

        * **getFileList** - return the files on a directory in
            **list** of pathlib.Path objects
        * **findFile** - find a file in the system Path
            return a pathlib.Path object if found
        * **getExecutable** - find executable file
            in PATH and the normal installation paths for Windows
            and macOS for linux is like findFile

    - classes

        * **RunCommand** - execute command in subprocess and capture
            output optionally apply regular expression searches
            and apply a supplied function to receive every line
            read and process them as needed
        * **ConfigurationSettings** - maintain a set of ConfigurationSettings
            in a **dictionary** and saved it in xml file

    - utilities

        * **mkvrun** - CLI utility to execute MKVToolNix_ generated
            command line.  MKVBatchMultiplex_ is a GUI implementation
            of this and the main reason this module goes public.
        * **apply2files** - apply a command to all files in the directory
            specified in recursive by default

and so on...

Installation
============

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

Main development platform is Windows but limited testing show they
work on Lin Linux and macOS.  The only OS specific is **vsutillib.macos**
but it run on other operating systems it won't raise exception
the results will mainly be **None**.

Dependencies
************

    * lxml_ 4.3.3 or greater on system
      XmlDB simple xml database
    * pymediainfo_ 4.0 or greater
    * Python_ 3.5->3.7
    * MediaInfo_ tested with versions 17.10->18.12.
      This is only for Linux a dependency of pymediainfo.


Usage
=====

Import the the library in your program:::

    from vsutillib import files
    from vsutillib import log
    from vsutillib import macos
    from vsutillib import media
    from vsutillib import network
    from vsutillib import process
    from vsutillib import xml


Roadmap
=======

Document all classes and functions.

.. Hyperlinks.

.. _pymediainfo: https://pypi.org/project/pymediainfo/
.. _Python: https://www.python.org/downloads/
.. _MKVToolNix: https://mkvtoolnix.download/
.. _Matroska: https://www.matroska.org/
.. _MediaInfo: https://mediaarea.net/en/MediaInfo
.. _AVI: https://docs.microsoft.com/en-us/windows/desktop/directshow/avi-file-format/
.. _SRT: https://matroska.org/technical/specs/subtitles/srt.html
.. _MKVBatchMultiplex: https://github.com/akai10tsuki/mkvbatchmultiplex
.. _`The TV Database`: https://www.thetvdb.com/
.. _`The Movie Database`: https://www.themoviedb.org/
.. _`ubuntu 18.04 LTS`: https://www.ubuntu.com/
.. _`macOS 10.14 Mojave`: https://www.apple.com/macos/mojave/
.. _`Windows 10`: https://www.microsoft.com/en-us/windows
.. _lxml: https://lxml.de/
