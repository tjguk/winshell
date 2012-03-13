@echo off
for /l %%n in (24,1,32) do if exist c:\python%%n\python.exe (echo. & echo python%%n & c:\python%%n\python.exe -W ignore test_winshell.py)
pause
