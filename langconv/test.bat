@echo off
set langconv=langconv.py

set dic=dic.xls
set tgt=LangID.h
echo =^> Generate a C header file (%tgt%) of language ID enumeration.
%langconv% lang_id -o%tgt% %dic%

set dic=dic.xls
set tgt=MsgID.h
echo =^> Generate a C header file (%tgt%) of message ID enumeration.
%langconv% msg_id -o%tgt% %dic%

set dic=dic.xls
set lst=char.lst
set tgt=verify.report
echo =^> Generate a report file (%tgt%) that lists used-but-not-listed
echo    chars and listed-but-not-used chars.
%langconv% verify -o%tgt% %dic% %lst%

set dic=dic.xls
set lst=char.lst
set tgt=mlang.i
echo =^> Generate a C included file (%tgt%) listing an array that packs
echo    multilanguage messages.
%langconv% pack -o%tgt% %dic% %lst%

pause
