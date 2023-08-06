
***************
Using vsutillib
***************

To import the library:

::

  import vsutillib

There are a few namespaces

::

  from vsutillib import mkv
  from vsutillib import media
  from vsutillib import mprocess

The **mkv** namespace is the more specific to MKVBatchMultiplex so the less
useful.  **media** have some classes/functions related to media files such as
**Movie** and **Series** to fetch information from `The TV Database`_ and
`The Movie Database`_. **mprocess** is for multithreading and multiprocessing
subclasses.

Requirements
============

The library is tested on Python_ 3.5->3.7 and Python_ 3.7 is the main
development version.  It works `ubuntu 18.04 LTS`_,
`macOS 10.14 Mojave`_ and `Windows 10`_.


Know Issues
===========

Interface is not set yet.


.. _Python: https://www.python.org/
.. _`The TV Database`: https://www.thetvdb.com/
.. _`The Movie Database`: https://www.themoviedb.org/
.. _`ubuntu 18.04 LTS`: https://www.ubuntu.com/
.. _`macOS 10.14 Mojave`: https://www.apple.com/macos/mojave/
.. _`Windows 10`: https://www.microsoft.com/en-us/windows
