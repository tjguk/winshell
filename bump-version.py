"""Bump the version of this project:

Look for likely files: setup.py, doc/conf.py, etc. and update
version strings to whatever's passed in. At present, no check
is made for sanity purposes.
"""
import os, sys
import re

patterns = [
  ("winshell.py", r'__VERSION__ = "[^"]+"', '__VERSION__ = "%s"'),
  ("docs/conf.py", r"version\s*=\s*'[^']+'", "version = '%s'"),
  ("docs/conf.py", r"release\s*=\s*'[^']+'", "release= '%s'"),
  ("setup.py", r'version = "[^"]+",', r'version = "%s",'),
]

def replace_version (filename, pattern, replacement):
  with open (filename) as inf:
    text = inf.read ()
  with open (filename, "w") as outf:
    outf.write (re.sub (pattern, replacement, text))

def main (new_version):
  for filename, pattern, replacement in patterns:
    if os.path.exists (filename):
      print "Rewriting ", filename
      replace_version (filename, pattern, replacement % new_version)

if __name__ == '__main__':
  main (*sys.argv[1:])
