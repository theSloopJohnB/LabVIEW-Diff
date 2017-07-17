SET vi1=%~f1
SET vi2=%~f2

REM only run if the file is a vi.

if "%vi1:~-3%" == ".vi" GOTO :DIFF_VI

GOTO :END


:DIFF_VI
    "C:\Program Files (x86)\National Instruments\LabVIEW 2014\LabVIEW.exe" C:\Users\nitest\Documents\GitHub\LabVIEW-Diff\Main.vi -- "%vi1%" "%vi2%" C:\Users\nitest\temp

:END