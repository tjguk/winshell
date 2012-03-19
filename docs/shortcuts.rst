Shortcuts
=========

..  module:: winshell
    :synopsis: Manage shell shortcuts
..  moduleauthor:: Tim Golden <mail@timgolden.me.uk>

The Windows Shell offers a facility -- properly called a Shell Link but most
commonly referred to as a shortcut -- to link
to a shell item, most commonly a file.  This is not the same as a hardlink or a symlink, bot
of which are implemented in an underlying file system. Shortcuts
are Shell objects which only behave differently when accessed
via a Shell interface (most commonly Windows Explorer) and can refer
to non-filesystem shell objects such as printers and networks.

Shortcuts are managed by means of a :class:`Shortcut` class. This is returned
from the :func:`shortcut` factory function which can be called with the path to a shortcut
file (typically ending in .lnk) which may or may not already exist, or
with the path to a target file. If the shortcut already exists, the
corresponding attributes will be populated inside the shortcut object.


..  py:function:: shortcut (path_or_object)

    Returns a :class:`Shortcut` object representing a shell link

    :param path_or_object: this is either an existing Shortcut object, in which
                           case it is returned unaltered, or the path to a file
                           which may or may not exist. If the path refers to an existing
                           shortcut, the returned object will represent that shortcut;
                           otherwise, the returned object will represent a shortcut to
                           that path.
    :returns: a :class:`Shortcut` object

..  py:class:: Shortcut

    An object which represents a shell link on the filesystem. The shell link
    may or may not already exist.

A :class:`Shortcut` object has the following attributes, each of which may be
read or written:

..  attribute:: Shortcut.arguments

    The arguments, if any, to the executable which this shortcut represents, if any

..  attribute:: Shortcut.description

    A long description for this shortcut, not immediately visible to the user
     can be used for storing arbitrary data).

..  attribute:: hotkey

    The hotkey for this shortcuts
    ..  TODO

..  attribute:: icon_location

    A two-tuple representing the file containing the icon and the position of the icon
    within that file's icon resources.

..  attribute:: path

    The target of the shortcut

..  attribute:: show_cmd

    One of: "normal" (the default), "minimized" and "maximized"

..

For backwards compatibility, the following function is exposed.

..  py:function:: CreateShortcut (Path, Target, Arguments="", StartIn="", Icon=("",0), Description="")

    Create a shortcut

    :param Path: As what file should the shortcut be created?
    :param Target: What command should the desktop use?
    :param Arguments: What arguments should be supplied to the command?
    :param StartIn: What folder should the command start in?
    :param Icon: (filename, index) What icon should be used for the shortcut?
    :param Description: What description should the shortcut be given?

    eg::

      CreateShortcut (
        Path=os.path.join (desktop (), "PythonI.lnk"),
        Target=r"c:\python\python.exe",
        Icon=(r"c:\python\python.exe", 0),
        Description="Python Interpreter"
      )

References
----------

..  seealso::

    `Shell Links Overview <http://msdn.microsoft.com/en-us/library/windows/desktop/bb776891%28v=vs.85%29.aspx>`_
      Shell Links on MSDN

To Do
-----

* More general-purpose implementation
* Allow reading & writing of shortcuts, possibly via a class mechanism