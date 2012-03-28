# -*- coding: UTF8 -*-
import os, sys
try:
  import ConfigParser
except ImportError:
  import configparser as ConfigParser
import filecmp
import operator
import shutil
import tempfile
import time
import unittest

try:
  from StringIO import StringIO
except ImportError:
  from io import StringIO

import pythoncom
from win32com.shell import shell, shellcon

import winshell

import test_base
if sys.version_info >= (2, 5):
  from test_winshell_25plus import *

try:
  unicode
except NameError:
  def b (s): return bytes (s, encoding="ascii")
else:
  def b (s): return str (s)

ini = ConfigParser.ConfigParser ()
ini.read ("testing_config.ini")

def get_config (section, item, function=ConfigParser.ConfigParser.get):
  if ini.has_option (section, item):
    return function (ini, section, item)
  else:
    return None

go_slow = bool (int (get_config ("general", "go_slow")))

class TestSpecialFolders (test_base.TestCase):
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

class TestFolderSupport (test_base.TestCase):

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

class TestFileOperations (test_base.TestCase):
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

  def test_copy_multifiles (self):
    from_filepath1, to_filepath1 = self.tempfiles (create_from=True, create_to=False)
    from_filepath2, to_filepath2 = self.tempfiles (create_from=True, create_to=False)
    winshell.copy_file ([from_filepath1, from_filepath2], [to_filepath1, to_filepath2])
    for from_filepath, to_filepath in zip ([from_filepath1, from_filepath2], [to_filepath1, to_filepath2]):
      self.files_are_equal (from_filepath, to_filepath)

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

class TestShortcuts (test_base.TestCase):

  #
  # Fixtures
  #
  def setUp (self):
    self.temppath = tempfile.mkdtemp ()
    self.targetpath = sys.executable
    self.lnkpath = os.path.join (self.temppath, "python.lnk")
    self.description = time.asctime ()

    sh = pythoncom.CoCreateInstance (
      shell.CLSID_ShellLink,
      None,
      pythoncom.CLSCTX_INPROC_SERVER,
      shell.IID_IShellLink
    )
    sh.SetPath (self.targetpath)
    sh.SetDescription (self.description)
    persist = sh.QueryInterface (pythoncom.IID_IPersistFile)
    persist.Save (self.lnkpath, 1)

  def tearDown (self):
    shutil.rmtree (self.temppath)

  #
  # Support functions
  #

  #
  # Tests
  #
  def test_CreateShortcut (self):
    shortcut_filepath = os.path.join (self.temppath, "32710ee1-6df9-11e1-8401-ec55f9f656d6")
    self.assertFalse (os.path.exists (shortcut_filepath))
    winshell.CreateShortcut (
      Path=shortcut_filepath,
      Target=sys.executable,
      Description = "32710ee1-6df9-11e1-8401-ec55f9f656d6"
    )
    self.assertTrue (os.path.exists (shortcut_filepath))

  #
  # Test factory function
  #
  def test_factory_none (self):
    self.assertIs (winshell.shortcut (None), None)

  def test_factory_no_param (self):
    shortcut = winshell.shortcut ()
    self.assertIsInstance (shortcut, winshell.Shortcut)
    self.assertTrue (shortcut.lnk_filepath is None)

  def test_factory_shortcut (self):
    shortcut = winshell.Shortcut ()
    self.assertIs (shortcut, winshell.shortcut (shortcut))

  def test_factory_from_link (self):
    shortcut = winshell.shortcut (self.lnkpath)
    self.assertFalse (shortcut.lnk_filepath is None)
    self.assertEqualCI (shortcut.lnk_filepath, self.lnkpath)
    self.assertEqualCI (shortcut.path, self.targetpath)

  def test_factory_from_target (self):
    shortcut = winshell.shortcut (self.targetpath)
    self.assertFalse (shortcut.lnk_filepath is None)
    self.assertEqualCI (shortcut.path, self.targetpath)

  #
  # Test utils
  #
  def test_dumped (self):
    #
    # Can't really do much for dump[ed] so just make sure they don't
    # crash & burn
    #
    self.assertTrue (winshell.shortcut ().dumped ().startswith ("{\n  -unsaved-"))

  def test_dump (self):
    #
    # Can't really do much for dump[ed] so just make sure they don't
    # crash & burn
    #
    _stdout = sys.stdout
    sys.stdout = StringIO ()
    try:
      winshell.shortcut ().dump ()
      sys.stdout.seek (0)
      self.assertTrue (sys.stdout.read ().startswith ("{\n  -unsaved-"))
    finally:
      sys.stdout = _stdout

class TestRecycler (test_base.TestCase):

  #
  # Fixtures
  #
  def setUp (self):
    self.root = os.path.join (tempfile.gettempdir (), "winshell")
    if not os.path.exists (self.root):
      os.mkdir (self.root)

    self.temppath = tempfile.mkdtemp (dir=self.root)
    handle, self.tempfile = tempfile.mkstemp (dir=self.temppath)
    os.close (handle)

    self.deleted_files = set ()
    f = open (self.tempfile, "wb")
    try:
      timestamp = b("*")
      f.write (timestamp)
    finally:
      f.close ()
    winshell.delete_file (self.tempfile, silent=True, no_confirm=True)

  def tearDown (self):
    shutil.rmtree (self.temppath)

  #
  # Support Functions
  #

  #
  # Tests
  #
  def test_factory_function (self):
    recycle_bin = winshell.recycle_bin ()
    self.assertIsInstance (recycle_bin, winshell.ShellRecycleBin)

  def test_empty (self):
    recycle_bin = winshell.recycle_bin ()
    recycle_bin.empty (confirm=False, show_progress=False, sound=False)
    self.assertFalse (list (recycle_bin))

  def test_iter (self):
    for item in winshell.recycle_bin ():
      if item.original_filename ().lower () == self.tempfile:
        break
    else:
      raise RuntimeError ("%s not found in recycle_bin" % self.tempfile)
    self.assertIsInstance (item, winshell.ShellRecycledItem)
    self.assertEqualCI (item.original_filename (), self.tempfile)

if go_slow:
  class TestRecyclerSlow (test_base.TestCase):

    #
    # Fixtures
    #
    def setUp (self):
      self.root = os.path.join (tempfile.gettempdir (), "winshell")
      if not os.path.exists (self.root):
        os.mkdir (self.root)

      self.temppath = tempfile.mkdtemp (dir=self.root)
      handle, self.tempfile = tempfile.mkstemp (dir=self.temppath)
      os.close (handle)

      self.deleted_files = set ()
      for i in range (3):
        f = open (self.tempfile, "wb")
        try:
          timestamp = b("*") * (i + 1)
          f.write (timestamp)
        finally:
          f.close ()
        self.deleted_files.add ((timestamp, os.path.getsize (self.tempfile)))
        winshell.delete_file (self.tempfile, silent=True, no_confirm=True)

        time.sleep (1.1)

    def tearDown (self):
      shutil.rmtree (self.temppath)

    def test_versions (self):
      recycle_bin = winshell.recycle_bin ()
      versions = recycle_bin.versions (self.tempfile)
      versions_info = set ()
      for version in versions:
        versions_info.add ((b("").join (version.contents ()), version.stat ()[2]))
      self.assertEqual (self.deleted_files, versions_info)

    def test_undelete (self):
      self.assertFalse (os.path.exists (self.tempfile))
      recycle_bin = winshell.recycle_bin ()
      newest = sorted (recycle_bin.versions (self.tempfile), key=lambda item: item.recycle_date ())[-1]
      newest_contents = b("").join (newest.contents ())
      recycle_bin.undelete (self.tempfile)
      self.assertTrue (os.path.exists (self.tempfile))
      self.assertEquals (open (self.tempfile, "rb").read (), newest_contents)

    def test_undelete_with_rename (self):
      self.assertFalse (os.path.exists (self.tempfile))
      recycle_bin = winshell.recycle_bin ()

      recycle_bin.undelete (self.tempfile)
      self.assertTrue (os.path.exists (self.tempfile))

      newest = sorted (recycle_bin.versions (self.tempfile), key=lambda item: item.recycle_date ())[-1]
      newest_contents = b("").join (newest.contents ())
      renamed_to = recycle_bin.undelete (self.tempfile)
      self.assertNotEqual (renamed_to, self.tempfile)
      self.assertTrue (os.path.exists (renamed_to))
      self.assertEquals (open (renamed_to, "rb").read (), newest_contents)

if __name__ == '__main__':
  unittest.main ()
