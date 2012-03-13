The winshell Module
*******************

What is it?
-----------

Certain aspects of the Windows user interface are grouped by
Microsoft as Shell functions. These include the Desktop, shortcut
icons, special folders (such as My Documents) and structured storage.
These are mostly available via the shell module of the pywin32
extensions, but whenever I need to use them, I've forgotten the
various constants and so on.

The module offers four areas of functionality:

* :doc:`special-folders`
* :doc:`file-operations`
* :doc:`shortcuts`
* :doc:`structured-storage`

Each of them is exposed by simple functions which offer sane defaults
for most of the options. Since it's perfectly possible to drop down to
the underlying win32com.shell functions, I haven't attempted to expose
every last option. It's entirely likely that future incarnations of this
module will be more ambitious.


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

The module has been tested on versions of Python from 2.4 to 3.2. It may also work
on older (or newer) versions.
It's tested with the most recent pywin32 extensions, but the functionality
it uses from those libraries has been in place for many versions.

