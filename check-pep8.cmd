@echo off
IF "%1" == "" (
	SET RUN_FROM="."
    GOTO run
)
SET RUN_FROM=%1

:run
python -mpep8 --max-line-length=120 --ignore=E401,E501,W292,E302,E261 %RUN_FROM%
pause