set c_dir=c_src

del %c_dir%\LangID.h
del %c_dir%\MsgID.h
del verify.report
del %c_dir%\mlang.i

rd /q /s %c_dir%\bin
rd /q /s %c_dir%\obj

cd c_src
make clean
cd ..
