@echo off
set langconv=langconv.py

set dic=dic.xls
set tgt=lang_id.h
echo =^> Generate a C header file (%tgt%) of language ID enumeration.
if not exist %dic% echo File "%dic%" Not Found!
if exist %dic% %langconv% lang_id -o%tgt% %dic%

set dic=dic.xls
set tgt=msg_id.h
echo =^> Generate a C header file (%tgt%) of message ID enumeration.
if not exist %dic% echo File "%dic%" Not Found!
if exist %dic% %langconv% msg_id -o%tgt% %dic%

set dic=dic.xls
set lst=char.lst
set tgt=verify.report
echo =^> Generate a report file (%tgt%) that lists used-but-not-listed
echo    chars and listed-but-not-used chars.
if not exist %dic% echo File "%dic%" Not Found!
if not exist %lst% echo File "%lst%" Not Found!
if exist %dic% if exist %lst% %langconv% verify -o%tgt% -l%lst% %dic%

set dic=dic.xls
set lst=char.lst
set tgt=mlang.i
echo =^> Generate a C included file (%tgt%) listing an array that packs
echo    multilanguage messages.
if not exist %dic% echo File "%dic%" Not Found!
if not exist %lst% echo File "%lst%" Not Found!
if exist %dic% if exist %lst% %langconv% pack -o%tgt% -l%lst% %dic%

pause
