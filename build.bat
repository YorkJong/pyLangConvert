@echo off

set bat_dir=%~dp0
cd /D %bat_dir%

set target=%1
if "%target%"=="" (
    set /p "target=Enter the target: "
)

:: split out the main filename
For %%A in ("%target%") do (
    set target=%%~nA
)

set src_dir=%target%

pyinstaller --onefile --distpath bin %src_dir%\%target%.py

del /Q %target%.spec
rd /Q /S build
del /Q *.pyc 2> NUL

if not "%2"=="SkipPause" pause
