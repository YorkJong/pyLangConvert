set c_dir=c_src

del %c_dir%\LangID.h
del %c_dir%\MsgID.h
del %c_dir%\mlang.i
del verify.report
del dic_trans.xls

rd /q /s %c_dir%\bin
rd /q /s %c_dir%\obj

cd c_src
make clean
cd ..
