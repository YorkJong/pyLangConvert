@echo off

set target=%1
if "%target%"=="" (
    set /p "target=Enter the target: "
)

set src_dir=%target%

pyinstaller --onefile %src_dir%\%target%.py

move dist\%target%.exe bin

del /Q %target%.spec
rem del /Q *.spec

rd /Q /S build
rd /Q /S dist

del *.pyc

if not "%2"=="SkipPause" pause