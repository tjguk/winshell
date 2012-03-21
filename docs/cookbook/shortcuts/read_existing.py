import os, sys
import glob
import winshell

for lnk in glob.glob (os.path.join (winshell.programs (), "*.lnk")):
  shortcut = winshell.shortcut (lnk)
  shortcut.dump ()
  break
else:
  print ("None found")