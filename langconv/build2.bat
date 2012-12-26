del %1.exe
set base=%Python_home%\Tools\pyinstaller-2.0

rem %base%\pyinstaller.py --onefile --strip %1.py
%base%\pyinstaller.py --onefile %1.py


move dist\%1.exe .

rem del /Q %1.spec
del /Q logdict*.log
del /Q *.spec

rd /Q /S build
rd /Q /S dist

del *.pyc

