import os, sys
import winshell

shortcut = winshell.shortcut (sys.executable)
shortcut.working_directory = "c:/temp"
shortcut.write (os.path.join (winshell.desktop (), "python.lnk"))
shortcut.dump ()