Structured Storage
==================

..  module:: winshell
    :synopsis: Manage structured storage
..  moduleauthor:: Tim Golden <mail@timgolden.me.uk>

The Windows Shell offers a slightly complicated facility to embed
its own metadata (or any other information) inside a file. This
concept is called Structured Storage and it's the basis for the
[Properties] tab available via Explorer. This can include data
from within the file's own structure (eg the ID3 tags from an MP3
file) but also data held separately, including arbitrary attributes,
which are held via structured storage.

The module currently implements the simplest of wrappers, querying
a file for any structured storage and retrieving any which is held
under the user-defined properties layout. (Structured storage can
hold data of several categories). Only specific, commonly-queried
fields are accessed, and they are returned as a Python dictionary.

Functions
---------

..  py:function:: structured_storage (filename)

    Determine any user-defined properties of this file, held as structured storage
    and return them as a dictionary.

    :param filename: What file is to be queried
    :returns: a dictionary containing commonly-used properties & values


References
----------

..  seealso::

    `Structured Storage <http://example.com>`_
      Structured storage on MSDN

To Do
-----

* More general-purpose implementation
* Allow writing of structured storage
