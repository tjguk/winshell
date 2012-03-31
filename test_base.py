# -*- coding: UTF8 -*-
import unittest

class TestCase (unittest.TestCase):

  def assertEqualCI (self, s1, s2, *args, **kwargs):
    self.assertEqual (s1.lower (), s2.lower (), *args, **kwargs)

  def assertIs (self, item1, item2, *args, **kwargs):
    self.assertTrue (item1 is item2, *args, **kwargs)

  def assertIsInstance (self, item, klass, *args, **kwargs):
    self.assertTrue (isinstance (item, klass), *args, **kwargs)

###