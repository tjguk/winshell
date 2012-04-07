REM
REM Run tests for all available versions of Python between 2.4 & 3.3
REM
@echo off
python -mpep8 --max-line-length=120 --ignore=E401,E501,W292,E302,E261 .
for /l %%n in (24,1,33) do if exist c:\python%%n\python.exe (echo. & echo python%%n & c:\python%%n\python.exe -W ignore test_winshell.py)
pause
