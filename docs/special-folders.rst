Special Folders
===============

..  module:: winshell
    :synopsis: Access special shell folders
..  moduleauthor:: Tim Golden <mail@timgolden.me.uk>

The Windows shell considers certain folders Special Folders (well-known
folders in newer versions). These include things like the Desktop folder,
My Documents, Program Files and so on. Although their locations are
generally pretty standard, it's good practice to access them via the
Shell API as they can be different on account of localisation, user
change, group policies, roaming profiles, etc.

The `winshell` module offers specific functions for the most common of
these plus a general-purpose function to access the remainder,
either by their numeric constant or by a text version of their name.
Where applicable, the specific functions can be called with a parameter
of `common` set to True. This will return the all-users version of the
folder.

Specific Functions
------------------

.. py:function:: desktop(common=True)

   Return the desktop folder

   :param common: whether to return the All Users folder
   :returns: the desktop folder

There are equivalent convenience functions for:

* application_data
* favourites
* bookmarks (alias of favourites)
* start_menu
* programs
* startup
* personal_folder
* my_documents (alias of personal_folder)
* recent
* sendto

The last three do not offer an "All Users" option via
the `common` parameter.

General Functions
-----------------

..  py:function:: folder(folder)

    Return the special folder corresponding to `folder`.

    :param folder: either the CSIDL_ numeric constant or the corresponding name,
                  eg "appdata" for CSIDL_APPDATA or "desktop" for CSIDL_DESKTOP.
    :returns: the corresponding filesystem folder

Example
-------

Copy all the shortcuts on your desktop to a newly-created folder in
the root of your profile::

  import os, sys
  import glob
  import winshell
  profile = winshell.folder ("profile")
  new_folder = os.path.join (profile, "TESTING")
  os.mkdir (new_folder)
  for f in glob.glob (os.path.join (winshell.desktop (), "*.lnk")):
    print ("Copying %s to %s" % (f, new_folder))
    winshell.copy_file (f, new_folder)

NB We're not doing anything fancy with the shell & shortcuts in this
example, simply assuming that shortcuts are files with an ".lnk" extension.

References
----------

..  seealso::

    `Special Folders <http://msdn.microsoft.com/en-us/library/windows/desktop/bb762494%28v=vs.85%29.aspx>`_
      Documentation on microsoft.com for well-known folders

To Do
-----

* New Vista / W7 Well-known folders via comtypes
* Programatically updating locations of well-known folders
