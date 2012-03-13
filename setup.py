from distutils.core import setup

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Environment :: Win32 (MS Windows)',
  'Intended Audience :: Developers',
  'Intended Audience :: System Administrators',
  'License :: OSI Approved :: MIT License',
  'Operating System :: Microsoft :: Windows',
  'Topic :: System :: Systems Administration',
  "Programming Language :: Python :: 2",
  "Programming Language :: Python :: 3",
]

long_description = """winshell
========

The winshell module is a light wrapper around the Windows shell functionality.

It includes convenience functions for accessing special folders, for using
the shell's file copy, rename & delete functionality, and a certain amount
of support for structured storage.

Docs are hosted at: http://winshell.readthedocs.org/
"""
setup (
  name = "winshell",
  version = "0.4.1",
  description = "Windows shell functions",
  author = "Tim Golden",
  author_email = "mail@timgolden.me.uk",
  url = "https://github.com/tjguk/winshell",
  license = "http://www.opensource.org/licenses/mit-license.php",
  py_modules = ["winshell"],
  long_description=long_description
)
