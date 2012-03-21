from __future__ import with_statement
import os, sys
import shutil
import tempfile
import time

import pythoncom
from win32com.shell import shell, shellcon

import winshell

import test_base

class TestContextManager (test_base.TestCase):

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
  # Tests
  #
  def test_context_manager (self):
    guid = "32710ee1-6df9-11e1-8401-ec55f9f656d6-2"
    shortcut_filepath = os.path.join (self.temppath, guid + ".lnk")
    self.assertFalse (os.path.exists (shortcut_filepath))
    with winshell.shortcut (shortcut_filepath) as s:
      s.path = self.targetpath
      s.description = guid
    self.assertTrue (os.path.exists (shortcut_filepath))
