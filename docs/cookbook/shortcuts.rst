.. currentmodule:: winshell
.. highlight:: python
   :linenothreshold: 1

Managing shortcuts
==================

.. _reading-details-from-an-existing-shortcut:

Reading details from an existing shortcut
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

