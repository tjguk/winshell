import os, sys
import filecmp
import shutil
import tempfile
import unittest

from win32com.shell import shell, shellcon

import winshell

class TestSpecialFolders (unittest.TestCase):
  #
  # It's genuinely difficult to test the special-folders functionality
  # without simply reproducing the code in the module (which is largely
  # a set of one-liners). At least at first, then, we're just going
  # to "exercise" the functions to ensure they run to successful completion
  # and produce an existing filepath. (In theory it would be possible for them
  # to produce a non-existent filepath but I'm not going to address that here).
  # Clearly this won't protect against, eg, a cut-and-paste which forgets to
  # change the original CSIDL constant.
  #

  #
  # Support methods
  #
  def assert_folder_exists (self, name, filepath):
    self.assertTrue (os.path.exists (filepath), "%s returns a non-existent filepath %s" % (name, filepath))
    self.assertTrue (os.path.isdir (filepath), "%s returns a filepath which is not a folder %s" % (name, filepath))

  #
  # Tests
  #
  def test_desktop (self):
    self.assert_folder_exists ("desktop personal", winshell.desktop (0))
    self.assert_folder_exists ("desktop common", winshell.desktop (1))

  def test_application_data (self):
    self.assert_folder_exists ("application_data personal", winshell.application_data (0))
    self.assert_folder_exists ("application_data common", winshell.application_data (1))

  def test_favourites (self):
    self.assert_folder_exists ("favourites personal", winshell.favourites (0))
    self.assert_folder_exists ("favourites common", winshell.favourites (1))

  def test_bookmarks (self):
    self.assert_folder_exists ("bookmarks personal", winshell.bookmarks (0))
    self.assert_folder_exists ("bookmarks common", winshell.bookmarks (1))

  def test_start_menu (self):
    self.assert_folder_exists ("start_menu personal", winshell.start_menu (0))
    self.assert_folder_exists ("start_menu common", winshell.start_menu (1))

  def test_programs (self):
    self.assert_folder_exists ("programs personal", winshell.programs (0))
    self.assert_folder_exists ("programs common", winshell.programs (1))

  def test_personal_folder (self):
    self.assert_folder_exists ("personal_folder", winshell.personal_folder ())

  def test_recent (self):
    self.assert_folder_exists ("recent", winshell.recent ())

  def test_sendto (self):
    self.assert_folder_exists ("sendto", winshell.sendto ())

class TestFolderSupport (unittest.TestCase):

  def test_get_path (self):
    self.assertEqual (winshell.get_path (shellcon.CSIDL_APPDATA), os.environ['APPDATA'])

  def test_get_folder_by_name (self):
    self.assertEqual (winshell.get_folder_by_name ("CSIDL_APPDATA"), os.environ['APPDATA'])

  def test_get_folder_by_name_no_prefix (self):
    self.assertEqual (winshell.get_folder_by_name ("APPDATA"), os.environ['APPDATA'])

  def test_get_folder_by_name_lowercase (self):
    self.assertEqual (winshell.get_folder_by_name ("appdata"), os.environ['APPDATA'])

  def test_get_folder_by_name_nonexistent (self):
    def _get_nonexistent_folder ():
      winshell.get_folder_by_name ("XXX")
    self.assertRaises (winshell.x_winshell, _get_nonexistent_folder)

  def test_folder_by_int (self):
    self.assertEqual (winshell.folder (shellcon.CSIDL_APPDATA), winshell.get_path (shellcon.CSIDL_APPDATA))

  def test_folder_by_name (self):
    self.assertEqual (winshell.folder ("CSIDL_APPDATA"), winshell.get_path (shellcon.CSIDL_APPDATA))

  def test_folder_by_name_no_prefix (self):
    self.assertEqual (winshell.folder ("APPDATA"), winshell.get_path (shellcon.CSIDL_APPDATA))

  def test_folder_by_name_lowercase (self):
    self.assertEqual (winshell.folder ("appdata"), winshell.get_path (shellcon.CSIDL_APPDATA))

  def test_folder_nonexistent (self):
    def _get_nonexistent_folder ():
      winshell.folder ("XXX")
    self.assertRaises (winshell.x_winshell, _get_nonexistent_folder)

class TestFileOperations (unittest.TestCase):
  #
  # It's also not easy to detect the more user-interfacey aspects of the
  # shell behaviour: whether the "flying folders" animation is operating,
  # or whether a user is prompted. This test case will do as much as it
  # can without having to involve the user. A more sophisticated setup
  # could use flags which indicate whether or not the test is being run
  # interactively.
  #

  #
  # Fixtures
  #
  def setUp (self):
    self.from_temppath = tempfile.mkdtemp ()
    self.to_temppath = tempfile.mkdtemp ()

  def tearDown (self):
    shutil.rmtree (self.from_temppath)
    shutil.rmtree (self.to_temppath)

  #
  # Support functions
  #
  def tempfiles (
    self,
    create_from=True, create_to=False,
    from_temppath=None, to_temppath=None
  ):
    from_temppath = from_temppath or self.from_temppath
    to_temppath = to_temppath or self.to_temppath
    from_filepath = tempfile.mktemp (prefix="from_", dir=from_temppath)
    if create_from:
      f = open (from_filepath, "wb")
      try:
        f.write (os.urandom (32))
      finally:
        f.close ()
      self.assertTrue (os.path.exists (from_filepath))
    else:
      self.assertFalse (os.path.exists (from_filepath))
    to_filepath = tempfile.mktemp (prefix="to_", dir=to_temppath)
    if create_to:
      open (to_filepath, "wb").close ()
      self.assertTrue (os.path.exists (to_filepath))
    else:
      self.assertFalse (os.path.exists (to_filepath))
    return from_filepath, to_filepath

  def files_are_equal (self, filepath1, filepath2):
    return filecmp.cmp (filepath1, filepath2, shallow=0)

  #
  # Tests
  #
  def test_simple_copy (self):
    from_filepath, to_filepath = self.tempfiles (create_from=True, create_to=False)
    winshell.copy_file (from_filepath, to_filepath)
    self.assertTrue (os.path.exists (to_filepath))
    self.assertTrue (self.files_are_equal (from_filepath, to_filepath))

  def test_copy_with_rename (self):
    from_filepath, to_filepath = self.tempfiles (create_from=True, create_to=True)
    winshell.copy_file (from_filepath, to_filepath, rename_on_collision=True)
    self.assertTrue (os.path.exists (to_filepath))
    self.assertFalse (self.files_are_equal (from_filepath, to_filepath))

    for filename in set (os.listdir (os.path.dirname (to_filepath))) - set ([os.path.basename (to_filepath)]):
      copy_of_filepath = os.path.join (os.path.dirname (to_filepath), filename)
      break

    self.assertTrue (self.files_are_equal (from_filepath, copy_of_filepath))

  def test_simple_move (self):
    from_filepath, to_filepath = self.tempfiles (create_from=True, create_to=False)
    f = open (from_filepath, "rb")
    try:
      from_contents = f.read ()
    finally:
      f.close ()
    winshell.move_file (from_filepath, to_filepath)
    self.assertFalse (os.path.exists (from_filepath))
    self.assertTrue (os.path.exists (to_filepath))
    f = open (to_filepath, "rb")
    try:
      self.assertEqual (from_contents, f.read ())
    finally:
      f.close ()

  def test_move_with_rename (self):
    from_filepath, to_filepath = self.tempfiles (create_from=True, create_to=True)
    f = open (from_filepath, "rb")
    try:
      from_contents = f.read ()
    finally:
      f.close ()
    winshell.move_file (from_filepath, to_filepath, rename_on_collision=True)

    for filename in set (os.listdir (os.path.dirname (to_filepath))) - set ([os.path.basename (to_filepath)]):
      copy_of_filepath = os.path.join (os.path.dirname (to_filepath), filename)
      break

    self.assertFalse (os.path.exists (from_filepath))
    self.assertTrue (os.path.exists (to_filepath))
    f = open (to_filepath, "rb")
    try:
      self.assertNotEqual (from_contents, f.read ())
    finally:
      f.close ()
    self.assertTrue (os.path.exists (copy_of_filepath))
    f = open (copy_of_filepath, "rb")
    try:
      self.assertEqual (from_contents, f.read ())
    finally:
      f.close ()

  def test_simple_rename (self):
    from_filepath, to_filepath = self.tempfiles (
      create_from=True, create_to=False,
      to_temppath=self.from_temppath
    )
    f = open (from_filepath, "rb")
    try:
      from_contents = f.read ()
    finally:
      f.close ()
    winshell.rename_file (from_filepath, to_filepath)
    self.assertFalse (os.path.exists (from_filepath))
    self.assertTrue (os.path.exists (to_filepath))
    f = open (to_filepath, "rb")
    try:
      self.assertEqual (from_contents, f.read ())
    finally:
      f.close ()

  def test_rename_with_rename (self):
    from_filepath, to_filepath = self.tempfiles (create_from=True, create_to=True, to_temppath=self.from_temppath)
    f = open (from_filepath, "rb")
    try:
      from_contents = f.read ()
    finally:
      f.close ()
    winshell.move_file (from_filepath, to_filepath, rename_on_collision=True)

    for filename in set (os.listdir (os.path.dirname (to_filepath))) - set ([os.path.basename (to_filepath)]):
      copy_of_filepath = os.path.join (os.path.dirname (to_filepath), filename)
      break

    self.assertFalse (os.path.exists (from_filepath))
    self.assertTrue (os.path.exists (to_filepath))
    f = open (to_filepath, "rb")
    try:
      self.assertNotEqual (from_contents, f.read ())
    finally:
      f.close ()
    self.assertTrue (os.path.exists (copy_of_filepath))
    f = open (copy_of_filepath, "rb")
    try:
      self.assertEqual (from_contents, f.read ())
    finally:
      f.close ()

  def test_simple_delete (self):
    from_filepath, to_filepath = self.tempfiles (
      create_from=True, create_to=False
    )
    winshell.delete_file (from_filepath, no_confirm=True)
    self.assertFalse (os.path.exists (from_filepath))

class TestShortcuts (unittest.TestCase):

  #
  # Fixtures
  #
  def setUp (self):
    self.temppath = tempfile.mkdtemp ()

  def tearDown (self):
    shutil.rmtree (self.temppath)

  #
  # Support functions
  #


  #
  # Tests
  #
  def test_create_shortcut (self):
    shortcut_filepath = os.path.join (self.temppath, "python.lnk")
    self.assertFalse (os.path.exists (shortcut_filepath))
    winshell.CreateShortcut (
      Path=shortcut_filepath,
      Target=sys.executable,
      Description = "Shortcut to Python"
    )
    self.assertTrue (os.path.exists (shortcut_filepath))

if __name__ == '__main__':
  unittest.main ()