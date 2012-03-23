# -*- coding: UTF8 -*-
from distutils.core import setup
import __winshell_version__ as __version__

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

#
# setup wants a long description which we'd like to read
# from README.rst; setup also wants a file called README
# github, however, wants a file called readme.rst. This
# is the compromise:
#
try:
  long_description = open ("README.rst").read ()
  open ("README", "w").write (long_description)
except (OSError, IOError):
   long_description = ""

setup (
  name = "winshell",
  version = __version__.__VERSION__ + __version__.__RELEASE__,
  description = "Windows shell functions",
  author = "Tim Golden",
  author_email = "mail@timgolden.me.uk",
  url = "https://github.com/tjguk/winshell",
  license = "http://www.opensource.org/licenses/mit-license.php",
  py_modules = ["winshell", "__winshell_version__"],
  long_description=long_description
)
