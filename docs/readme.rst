The winshell Module
*******************

What is it?
-----------

Certain aspects of the Windows user interface are grouped by
Microsoft as Shell functions. These include the Desktop, shortcut
icons, special folders (such as My Documents) and a few other things.
These are mostly available via the shell module of the pywin32
extensions, but whenever I need to use them, I've forgotten the
various constants and so on.

Several of the shell items have two variants: personal and common,
or User and All Users. These refer to systems with profiles in use:
anything from NT upwards, and 9x with Profiles turned on. Where
relevant, the Personal/User version refers to that owned by the
logged-on user and visible only to that user; the Common/All Users
version refers to that maintained by an Administrator and visible
to all users of the system.

There are other generally useful functions which are grouped under
the heading of shell-related, for example moving & copying files
with animated progress icons and deleting them into the system
recycle bin.

The module offers four areas of functionality:

* :doc:`special-folders`
* :doc:`file-operations`
* :doc:`shortcuts`
* Structured Storage


Where do I get it?
------------------

* Source: https://github.com/tjguk/winshell
* Release: http://pypi.python.org/pypi/winshell


Copyright & License?
--------------------

(c) Copyright Tim Golden <mail@timgolden.me.uk> 2012
Licensed under the (GPL-compatible) MIT License:
http://www.opensource.org/licenses/mit-license.php


Prerequisites
-------------

The module has been tested on versions of Python from 2.4 to 3.2. It may work
on older (or newer) versions but I don't have those installed for testing.
It's tested with the most recent pywin32 extensions, but the functionality
it uses from those libraries has been in place for many versions.

