Recycle Bin
===========

..  module:: winshell
    :synopsis: Manage shell shortcuts
..  moduleauthor:: Tim Golden <mail@timgolden.me.uk>

The Windows Shell allows file to be deleted which can then be retrieved
later, as though picked out of a rubbish bin. This funcionality is exposed
here by means of the :class:`ShellRecycleBin` class which allows the items in
the bin to be enumerated. Each item has methods which return its original
filepath and the date/time at which it was recycled. This is especially
important because the same item (that is: an item with the same filepath)
can appear multiple times in the recycle bin having been recreated and
deleted several times.

Once the appropriate item has been determined, it can be restored to its
original place in the filesystem. This restore is done by means of a
rename-on-collision move, so if a file of the same name already exists
in the original directory, the restored version will be renamed to
"Copy of..." or something similar, depending on which version of Windows
you're running. The restored filename is returned from the function.

If what you want to do is to undelete the latest version of a file,
then you're looking for the :func:`undelete`
convenience which can be called several times in succession in case you're
not sure which version you're after. So::

  import os, sys
  import winshell

  filepath = os.path.abspath ("test.txt")
  #
  # You create a file and delete it
  #
  with open (filepath, "w") as f:
    f.write ("test1")
  winshell.delete_file (filepath)

  #
  # Then you create a newer version and delete that
  #
  with open (filepath, "w") as f:
    f.write ("test2")
  winshell.delete_file (filepath)

  #
  # Finally you create the newest version
  #
  with open (filepath, "w") as f:
    f.write ("test3")

  recycle_bin = winshell.recycle_bin ()
  print (recycle_bin.versions (filepath))

  #
  # Now you undelete the previous versions which
  # will be renamed as "Copy of..." or something similar.
  #
  print winshell.undelete (filepath)
  print winshell.undelete (filepath)


..  py:function:: recycle_bin

    Returns a :class:`ShellRecycleBin` object representing the system Recycle Bin

..  py:function:: undelete (filepath)

    Find the most recent version of `filepath` to have been recycled and
    restore it to its original location on the filesystem. If a file already
    exists at that filepath, the copy will be renamed. The resulting filepath
    is returned.

..  py:class:: ShellRecycleBin

    An object which represents the union of all the recycle bins on this
    system. The Shell subsystem doesn't offer any way to access drive-specific
    bins (except by coming across them "accidentally" as shell folders within
    their specific drives).

    The object (which is returned from a call to :func:`recycle_bin`) is
    iterable, returning the deleted items wrapped in :class:`ShellRecycledItem`
    objects. It also exposes a couple of common-need convenience methods:
    :meth:`versions` returns a list of all recycled versions of a given original
    filepath; and :meth:`restore_newest` which restores the most-recently
    binned version of a given original filepath.

    The object has the following methods:

    ..  method:: empty (confirm=True, show_progress=True, sound=True)

        Empty all system recycle bins, optionally prompting for confirmation,
        showing progress, and playing a sort of crunching sound.

    ..  method:: undelete (filepath)

        cf :func:`undelete` which is a convenience wrapper around this method.

    ..  method:: versions (filepath)

        Return a (possibly empty) list of all recycled versions of a given
        filepath. Each item in the list is a :class:`ShellRecycledItem`.

..  py:class:: ShellRecycledItem

    An object representing one version of a file held in a recycle bin. The
    item's original filepath and the date/time it was deleted can be accessed
    as well as the underlying filename within the recycle bin folder. The item's
    contents can be retrieved and it can be restored to its original position.

    The object has the following methods:

    ..  method:: original_filename

        Return the original filepath of the object when it was deleted

    ..  method:: recycle_date

        Return a Python datetime instance representing the moment in which the
        file was deleted.

    ..  method:: contents (buffer_size=8192)

        Return an iterator over the data in the file, chunked up into
        `buffer_size` chunks.

    ..  method:: undelete

        Implements the undelete functionality used by :func:`undelete`, returning
        any remapping which has occurred because of collision renaming.

References
----------

..  seealso::

    :doc:`cookbook/recycle-bin`
      Cookbook examples of using the recycle bin
