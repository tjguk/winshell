REM
REM Run tests for all available versions of Python between 2.4 & 3.3
REM
@echo off
for /l %%n in (24,1,33) do if exist c:\python%%n\python.exe (echo. & echo python%%n & c:\python%%n\python.exe -W ignore test_winshell.py)
pause
