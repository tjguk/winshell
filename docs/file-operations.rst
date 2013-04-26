File Operations
===============

..  module:: winshell
    :synopsis: Copy, rename & delete files
..  moduleauthor:: Tim Golden <mail@timgolden.me.uk>

The Windows shell offers functionality (exposed via Explorer)
to allow files to be copied, renamed and deleted. This includes
features such as an animated progress display, automatic renaming
on conflict ("Copy of...") and the ability to use the Recycle Bin.

Functions
---------

Three functions are exposed with very similar signatures:

.. py:function:: copy_file(source_path, target_path, allow_undo=True, no_confirm=False, rename_on_collision=True, silent=False, extra_flags=0, hWnd=None)

   Use shell functionality to copy a file, optionally with animation, collision
   renaming and specifying a window to run against.

   :param source_path: a single or a list of simple or wildcard file specifications
   :param target_path: a single or a list of simple or wildcard file or folder specifications
   :param allow_undo: whether to enable Explorer to reverse this operation
   :param no_confirm: whether to overwrite a file without asking
   :param rename_on_collision: whether to generate an automatically-renamed alternative when the target_path already exists
   :param silent: whether to hide the animated display
   :param extra_flags: an integer which will be OR-ed into the flags parameter of SHFileOperation
   :param hWnd: against which window handle to display any animated dialog

.. py:function:: move_file(source_path, target_path, allow_undo=True, no_confirm=False, rename_on_collision=True, silent=False, extra_flags=0, hWnd=None)

   Use shell functionality to move a file, optionally with animation, collision
   renaming and specifying a window to run against.

   :param source_path: a single or a list of simple or wildcard file specifications
   :param target_path: a single or a list of simple or wildcard file or folder specifications
   :param allow_undo: whether to enable Explorer to reverse this operation
   :param no_confirm: whether to overwrite a file without asking
   :param rename_on_collision: whether to generate an automatically-renamed alternative when the target_path already exists
   :param silent: whether to hide the animated display
   :param extra_flags: an integer which will be OR-ed into the flags parameter of SHFileOperation
   :param hWnd: against which window handle to display any animated dialog

.. py:function:: rename_file(source_path, target_path, allow_undo=True, no_confirm=False, rename_on_collision=True, silent=False, extra_flags=0, hWnd=None)

   Use shell functionality to rename a file, optionally with animation, collision
   renaming and specifying a window to run against.

   :param source_path: a single or a list of simple or wildcard file specifications
   :param target_path: a single or a list of simple or wildcard file or folder specifications
   :param allow_undo: whether to enable Explorer to reverse this operation
   :param no_confirm: whether to overwrite a file without asking
   :param rename_on_collision: whether to generate an automatically-renamed alternative when the target_path already exists
   :param silent: whether to hide the animated display
   :param extra_flags: an integer which will be OR-ed into the flags parameter of SHFileOperation
   :param hWnd: against which window handle to display any animated dialog


  source_path,
  allow_undo=True,
  no_confirm=False,
  silent=False,
  extra_flags=0,
  hWnd=None

.. py:function:: delete_file(source_path, allow_undo=True, no_confirm=False, silent=False, extra_flags=0, hWnd=None)

   Use shell functionality to delete a file, optionally with animation, collision
   renaming and specifying a window to run against.

   :param source_path: a single or a list of simple or wildcard file specifications
   :param allow_undo: whether to enable Explorer to reverse this operation
   :param no_confirm: whether to overwrite a file without asking
   :param silent: whether to hide the animated display
   :param extra_flags: an integer which will be OR-ed into the flags parameter of SHFileOperation
   :param hWnd: against which window handle to display any animated dialog

References
----------

..  seealso::

    `The SHFileOperation function <http://msdn.microsoft.com/en-us/library/windows/desktop/bb762164%28v=vs.85%29.aspx>`_
      The SHFileOperation function on MSDN
