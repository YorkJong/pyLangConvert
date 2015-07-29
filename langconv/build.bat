del %1.exe
pyinstaller --onefile %1.py

move dist\%1.exe .

del /Q %1.spec
rem del /Q *.spec

rd /Q /S build
rd /Q /S dist

del *.pyc

