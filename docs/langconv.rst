===========
LangConvert
===========
-------------------
Language Converting
-------------------

:Author: Jiang Yu-Kuan
:Contact: yukuan.jiang@gmail.com
:Revision: 0005
:Date: 2016-01-26

.. contents::


Introduction
============

LangConvert is an open source Python application to generate multi-language
relative files for application on embedded systems. With an Excel dictionary
file, it can enumerate language IDs and message IDs with the format of C header
files. With an additional character list file, it can help us indexing
characters and packing messages.

Usage
=====
Top level
---------
usage: langconv.exe [-h] [-v] {lang_id,msg_id,verify,pack} ...

positional arguments:
  {lang_id,msg_id,verify,pack}
                        commands
    lang_id             Generate a C header file of language ID enumeration.
    msg_id              Generate a C header file of message ID enumeration.
    verify              Generate a report file that lists used-but-not-listed
                        characters and listed-but-not-used characters.
    pack                Generate a C included file listing an array that packs
                        multilanguage messages.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

lang_id command
---------------
usage: langconv.exe lang_id [-h] [-o <file>] XLS-file

positional arguments:
  XLS-file              An Excel dictionary file for multilanguage
                        translation.

optional arguments:
  -h, --help            show this help message and exit
  -o <file>, --output <file>
                        place the output into <file>, a C header file (default
                        "LangID.h").

msg_id command
--------------
usage: langconv.exe msg_id [-h] [-o <file>] XLS-file

positional arguments:
  XLS-file              An Excel dictionary file for multilanguage
                        translation.

optional arguments:
  -h, --help            show this help message and exit
  -o <file>, --output <file>
                        place the output into <file>, a C header file (default
                        "MsgID.h").

verify command
--------------
usage: langconv.exe verify [-h] [-o <file>] XLS-file LST-file

positional arguments:
  XLS-file              An Excel dictionary file for multilanguage
                        translation.
  LST-file              An unicode text file that lists unicode characters.

optional arguments:
  -h, --help            show this help message and exit
  -o <file>, --output <file>
                        place the output into <file>, an unicode text file
                        (default "verify.report").

pack command
------------
usage: langconv.exe pack [-h] [-o <file>] XLS-file LST-file

positional arguments:
  XLS-file              An Excel dictionary file for multilanguage
                        translation.
  LST-file              An unicode text file that lists unicode characters.

optional arguments:
  -h, --help            show this help message and exit
  -o <file>, --output <file>
                        place the output into <file>, a C included file
                        (default "mlang.i").


ToDo List
=========


Version History
===============
1.05
----
Released 2012-12-25

* Changed default output filename of lang_id command to "LangID.h"
* Changed default output filename of msg_id command to "MsgID.h"
* Renamed enum MsgId to MsgID
* Refined wrap_header_guard


1.00
----
Released 2012-12-03

* Initial version
