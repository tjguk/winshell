import os, sys
import winshell

shortcut = winshell.shortcut (sys.executable)
shortcut.write (os.path.join (winshell.desktop (), "python.lnk"))
shortcut.write (os.path.join (winshell.programs (), "python.lnk"))
