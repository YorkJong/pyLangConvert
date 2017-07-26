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
rem del /Q *.spec

rd /Q /S build
rd /Q /S dist

del *.pyc

if not "%2"=="SkipPause" pause
