Shortcuts
=========

..  module:: winshell
    :synopsis: Manage shell shortcuts
..  moduleauthor:: Tim Golden <mail@timgolden.me.uk>

The Windows Shell offers the ability to link to files via a
shortcut. This is not the same as a hardlink or a symlink, both
of which are implemented in an underlying file system. Shortcuts
are Shell objects which only behave differently when accessed
via a Shell interface (most commonly Windows Explorer).

Functions
---------

Only one function is exposed at present.

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