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

If you just need to perform some action over each files (as opposed to bringing them
all together into an in-memory structure) then iterate over the recycle bin.

If you just want the versions of some specific original file, you
want the :meth:`ShellRecycleBin.versions` function.


..  _undelete-by-criteria:

Undelete by criteria
--------------------

Undelete only those .txt files which were deleted today.

..  literalinclude:: recycle-bin/undelete_by_criteria.py

Discussion
~~~~~~~~~~

Iterating over a :class:`ShellRecycleBin` yields :class:`ShellRecycledItem` objects
in no particular order, each one representing a file deleted from a particular path
at a particular time. These objects expose :meth:`ShellRecycledItem.original_filename`
and :meth:`ShellRecycledItem.recycle_date` representing the name of the file when it
was deleted and the timestamp of that event.

It's possible for a file at the same path to be deleted multiple times before the
recycle bin is emptied. When undeleting these files a copy is generated in the
original folder based on the original name.