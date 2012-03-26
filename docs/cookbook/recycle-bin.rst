.. currentmodule:: winshell
.. highlight:: python
   :linenothreshold: 1

Recycle Bin
===========

.. _list-all-deleted-files:

List all deleted files
----------------------

List all the versions of all the files which are in the Recycle Bin.

..  literalinclude:: recycle-bin/list_all_deleted_files.py

Discussion
~~~~~~~~~~
The :func:`recycle_bin` factory function returns a :class:`ShellRecycleBin`
object which represents the union of all drive-specific recycle bins on the
system. (It's not possible AFAICT to select only one). This objects is iterable,
yielding one :class:`ShellRecycledItem` for each version of each file contained
in the bin.

If you just want the versions of some specific original file, you
want the :meth:`ShellRecycleBin.versions` function.

