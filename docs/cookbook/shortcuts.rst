.. currentmodule:: winshell
.. highlight:: python
   :linenothreshold: 1

Managing shortcuts
==================

.. _read-details-from-an-existing-shortcut:

Read details from an existing shortcut
-----------------------------------------

Open an existing shortcut and output its details: the target,
the window mode, any arguments, &c.

..  literalinclude:: shortcuts/read_existing.py

Discussion
~~~~~~~~~~
The :func:`shortcut` factory function accepts various items as
its one argument. If the argument is a string and points to a
shell link on disk, the shortcut is wrapped and the result
:class:`Shortcut` object returned.

The :meth:`Shortcut.dump` function is a convenience function which
returns the values of each of the settable attributes in a dict-like
layout.


.. _create-a-shortcut-to-a-file:

Create a shortcut to a file
---------------------------

Create a shortcut on the desktop which points to the Python
executable, setting the working directory to c:\temp.

..  literalinclude:: shortcuts/create_shortcut_to_file.py

Discussion
~~~~~~~~~~
The :func:`shortcut` factory function accepts various items as
its one argument. If the argument is a string and does not point
to a shell link on disk, the argument is taken to be the target
for a new :class:`Shortcut` object.

The :func:`desktop` function returns the filesystem path to
the user's desktop.

The :meth:`Shortcut.write` method creates a shortcut at the
location given.


..  _create-a-shortcut-in-multiple-locations:

Create a shortcut in multiple locations
---------------------------------------

Create the same shortcut on the user's desktop and in the Programs
folder.

..  literalinclude:: shortcuts/create_multiple_shortcuts.py


..  _walk-the-programs-tree-and-list-shortcut-targets:

Walk the programs tree and list the shortcut targets
----------------------------------------------------

Walk the Start Menu Programs tree and list, for each shortcut,
the shortcut name and its target along with any parameters.

..  literalinclude:: shortcuts/walk_program_tree.py

Discussion
~~~~~~~~~~
The Start Menu merges shortcuts from two folders: the user Programs
folder and the common Programs folder. We first scan the user Programs
folder, building up a dictionary mapping relative path name to a
list of shortcut objects representing the icons within. We then carry
out the equivalent action for the common Programs file, merging the
results into the same dictionary.

The result is a simple ASCII tree of folders, links and subfolders, including
links from user and common installs.