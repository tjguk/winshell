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

..  autofunction:: desktop
..  autofunction:: common_desktop
..  autofunction:: application_data
..  autofunction:: favourites
..  autofunction:: bookmarks
..  autofunction:: start_menu
..  autofunction:: programs
..  autofunction:: startup
..  autofunction:: personal_folder
..  autofunction:: my_documents
..  autofunction:: recent
..  autofunction:: sendto

General Functions
-----------------

..  autofunction:: folder

References
----------

..  seealso::

    `Special Folders <http://msdn.microsoft.com/en-us/library/windows/desktop/bb762494%28v=vs.85%29.aspx>`_
      Documentation on microsoft.com for well-known folders

To Do
-----

* New Vista / W7 Well-known folders via comtypes
* Programatically updating locations of well-known folders
