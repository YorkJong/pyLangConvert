del %1.exe
set base=%Python_home%\Tools\pyinstaller-1.5.1
%base%\Makespec.py --onefile --upx %1.py
%base%\Build.py %1.spec

move .\dist\%1.exe .

@echo off
del /Q %1.spec
del /Q warn%1.txt
rem del *.pyc

rd /Q /S build
rd /Q /S dist
del /Q logdict*.log
