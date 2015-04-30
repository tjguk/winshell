import os, sys
import winshell

c = winshell.Console()
while True:
    c.write(">>> ")
    line = ""
    while True:
        event = c.event()
        if event.EventType != 1:
            continue
        if event.VirtualKeyCode == 13:
            break
        elif 32 <= event.VirtualKeyCode <= 128:
            c.write(event.Char)
            line += event.Char
        else:
            continue
    
    c.write("You said: %s\n" % line)
