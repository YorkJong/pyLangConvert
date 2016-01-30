@echo off
set langconv=langconv.exe
set c_dir=c_src

set src=dic_empty.xls
set tgt=dic_trans.xls
echo =^> Generate a translated Excel file (%tgt%).
%langconv% trans_dic -o%tgt% %src%

pause
