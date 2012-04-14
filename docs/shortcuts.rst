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
    may or may not already exist. The object acts as its own context manager,
    allowing an existing shortcut to be modified in-place, or a new one created::

        import os, sys
        import winshell

        link_filepath = os.path.join(winshell.desktop(), "python.lnk")
        with winshell.shortcut(link_filepath) as link:
          link.path = sys.executable
          link.description = "Shortcut to python"
          link.arguments = "-m winshell"


    The object has the following attributes. For the shortcut to make
    any sense, you must set :attr:`Shortcut.path`. In addition,
    :attr:`Shortcut.lnk_filepath` must either be set explicitly by
    assigning it a filepath or implicitly as the source of the
    :class:`Shortcut` object or via the :meth:`Shortcut.write` method.

    ..  attribute:: Shortcut.lnk_filepath

        The location of the shortcut (the .lnk file) on the filesystem

    ..  attribute:: Shortcut.path

        The target of the shortcut

    ..  attribute:: Shortcut.arguments

        The arguments, if any, to the executable which this shortcut represents, if any

    ..  attribute:: Shortcut.description

        A long description for this shortcut, not immediately visible to the user
         can be used for storing arbitrary data).

    ..  attribute:: Shortcut.hotkey

        The hotkey for this shortcuts
        ..  TODO

    ..  attribute:: Shortcut.icon_location

        A two-tuple representing the file containing the icon and the position of the icon
        within that file's icon resources.

    ..  attribute:: Shortcut.show_cmd

        One of: "normal" (the default), "min" and "max"

    ..  attribute:: Shortcut.working_directory

        The directory which should be made active before the shortcut's
        target is executed.

    The object has the following methods:

    ..  method:: dump (level=0)

        Write to sys.stdout a summary of the shortcut's attributes offset by (level * 2) spaces

    ..  method:: dumped (level=0)

        Return a string representing a summary of the shortcut's attributes offset by (level * 2) spaces

    ..  method:: write (filepath=None)

        Create or update the underlying shell link to disk. If `filepath` is given, the
        link is created there; otherwise, the shortcut's original location is used. If
        the object was not created from a shortcut and has no location, an :exc:`x_shell`
        exception is raised.

For backwards compatibility, the following function is exposed:

..  py:function:: CreateShortcut (Path, Target, Arguments="", StartIn="", Icon=("",0), Description="")

    Create a shortcut

    :param Path: As what file should the shortcut be created?
    :param Target: What command should the desktop use?
    :param Arguments: What arguments should be supplied to the command?
    :param StartIn: What folder should the command start in?
    :param Icon: (filename, index) What icon should be used for the shortcut?
    :param Description: What description should the shortcut be given?

    eg::

      winshell.CreateShortcut(
        Path=os.path.join(desktop(), "PythonI.lnk"),
        Target=r"c:\python\python.exe",
        Icon=(r"c:\python\python.exe", 0),
        Description="Python Interpreter"
      )

but new code should use the :func:`shortcut` factory function and a with-block
to update or create a shortcut::

  desktop = winshell.desktop()
  with winshell.shortcut(os.path.join(desktop, "PythonI.lnk")) as shortcut:
    shortcut.path = sys.executable
    shortcut.icon = sys.executable, 0
    shortcut.description = "Python Interpreter"

References
----------

..  seealso::

    :doc:`cookbook/shortcuts`
      Cookbook examples of using shortcuts

    `Shell Links Overview <http://msdn.microsoft.com/en-us/library/windows/desktop/bb776891%28v=vs.85%29.aspx>`_
      Shell Links on MSDN
