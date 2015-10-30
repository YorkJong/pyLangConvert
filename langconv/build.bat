
set target=%1
if "%target%"=="" (
    set /p target=Enter the target:
)

del %target%.exe
pyinstaller --onefile %target%.py

move dist\%target%.exe .

del /Q %target%.spec
rem del /Q *.spec

rd /Q /S build
rd /Q /S dist

del *.pyc

