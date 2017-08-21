@SET vi1=%~f1
@SET vi2=%~f2

@REM only run if both files are VIs.

@if "%vi1:~-3%" == ".vi" (
    if "%vi2:~-3%" == ".vi" GOTO :DIFF_VI
)
GOTO :END


:DIFF_VI
    labview-cli --kill --lv-ver 2014 C:\Users\nitest\Documents\GitHub\LabVIEW-Diff\Main.vi -- "%vi1%" "%vi2%"  C:\Users\nitest\temp

:END