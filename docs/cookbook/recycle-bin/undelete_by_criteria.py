import os
import datetime
import fnmatch
import winshell

midnight = datetime.datetime.today ().replace (hour=0, minute=0, second=0)
for item in winshell.recycle_bin ():
  if fnmatch.fnmatch (os.path.basename (item.original_filename ()), "*.txt"):
    if item.recycle_date () >= midnight:
      print ("About to undelete %r" % item)
