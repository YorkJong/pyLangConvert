# LangConvert #

LangConvert is an open source Python application to generate multi-language
relative files for applications on embedded systems. With an Excel dictionary
file, it can enumerate language IDs and message IDs with the format of C header
files. With an additional character list file, it can help us indexing
characters and packing messages.


## Install ##

1. Download a binary distribution of LangConvert (e.g.,
   *LangConvert-1.06-bin.zip*) from [Downloads][] page.
2. Uncompress the binary distribution.

[Downloads]: https://bitbucket.org/YorkJong/pylangconvert/downloads


## Getting Started ##

1. Install LangConvert.
2. Edit the *dic.xls*
    - The Excel dictionary file provides language translations for each
      messages.
    - LangConvert uses the file to enumerate language IDs (see *LangID.h*)
      and to enumerate message IDs (see *MsgID.h*).
3. Edit the *char.lst* or just create an empty *char.lst*.
    - The character list file is used to decide orders of characters
    - LangConvert uses the file to index characters and pack messages (see
      *mlang.i*).
4. Run `demo.bat`.
    - This will generate *LangID.h*, *MsgID.h*, *malng.i* in *c_src* directory.
    - And generate *verify.report*.
5. Refined *char.lst* according to the *verify.report*.

### Note ###
- Run `demo_trans.bat` to translate messages in *dic_empty.xls* and
  output *dic_trans.xls*
- Run `clean.bat` to remove the generated files.

### A screenshot of *dic.xls* ###
![dic.xls.png](https://bitbucket.org/repo/kXE4Bp/images/721654582-dic.xls.png)

- The spreadsheet shown above has 20 rows and eight columns (A-H).
- Row 2 is the header row listing languae names.
- Column B is message-ID column. An empty cell in the column means the ID of
  this message is the same with English message.
- The `x` in Cell A9 (Column A, Row 9) denotes Row 9 a comment (So do A10).

### A sample *char.lst* ###
```sh
# A sample character list file

:0x20
 !"#$%&'()*+,-./0123456789:;<=>?
@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_
`abcdefghijklmnopqrstuvwxyz{|}~

:0xA0
áíñóúąćęśП
РУЭабвдежз
ийклмнопрс
туфщыьэюя中
件像册删单图子定客影
文时显检此电相示置菜
言设访语间除验간겠국
까뉴니메문미방범삭설
스습시앨어언영을이인
일자전정제지틸파표하
한화확？
```
- The character-list file lists characters that may be used in multilingual
  messages.
- A line prefixing `#` denotes a comment line.
- A line prefixing `:` denotes an offset of character indexing.
    - `:0X20` means the index of the next character ` ` (space) is 0x20 (same
      with space's ASCIll code), `!` 0x21, `"` 0x22, and so on.
    - `:0xA0` means the index of next character `á` is 0xA0, `í` 0xA1, and so
      on.

### The generated *verify.report* ###
```sh
# Generated by the Multi-language converting tool v1.05
#    !author: Jiang Yu-Kuan <yukuan.jiang@gmail.com>
#    !trail: langconv.exe verify -overify.report dic.xls char.lst

# Chars listed but not used:
!"#$%&'()*
+,-./01234
56789:;<=>
@JQWXZ[\]^
_`qx{|}~
```
- A report file lists two kind of characters:
    1. Characters list in *char.lst* but are not used in *dic.xls*.
    2. Characters are used in *dic.xls* but do not list in *char.lst*.
- The above report file only lists case 1; that means that the *char.lst*
  does not miss any character used in the *dic.xls*
- A line prefixing `#` denotes a comment line.

### The generated *LangID.h* ###
```c
// Generated by the Multi-language converting tool v1.05
//    !author: Jiang Yu-Kuan <yukuan.jiang@gmail.com>
//    !trail: langconv.exe lang_id -oc_src\LangID.h dic.xls
#ifndef _LANG_ID_H
#define _LANG_ID_H


/** Language Indexes */
typedef enum {
    L_English,
    L_Chinese,
    L_Korean,
    L_Spanish,
    L_Russian,
    L_Polish,
    L_End,
    L_Total = L_End
} Lang;


#endif // _LANG_ID_H
```
- The above is a C header file enumerating language names.
- The language names are extracted from the header row of the spreadsheet
  (i.e., *dic.xls*).

### The generated *MsgID.h* ###
```c
// Generated by the Multi-language converting tool v1.05
//    !author: Jiang Yu-Kuan <yukuan.jiang@gmail.com>
//    !trail: langconv.exe msg_id -oc_src\MsgID.h dic.xls
#ifndef _MSG_ID_H
#define _MSG_ID_H


/** IDs of Messages */
typedef enum {
    MSG_English,
    MSG_Chinese,
    MSG_Korean,
    MSG_Spanish,
    MSG_Russian,
    MSG_Polish,
    MSG_CheckingVisitor,
    MSG_MenuSetting,
    MSG_ElectronicAlbum,
    MSG_DeleteThisFileQ,
    MSG_TimeSetting,
    MSG_DisplaySetting,
    MSG_LanguageSetting,
    MSG_SETTING,
    MSG_MOVIE,
    MSG_StillImage,
    MSG_End,
    MSG_Total = MSG_End
} MsgID;


#endif // _MSG_ID_H
```
- The above is a C header file enumerating message IDs.
- The message IDs are extracted from the ID column of the spreadsheet (i.e.,
  *dic.xls*).

### A segment of the generated *mlang.i* ###
```c
// Generated by the Multi-language converting tool v1.05
//    !author: Jiang Yu-Kuan <yukuan.jiang@gmail.com>
//    !trail: langconv.exe pack -oc_src\mlang.i dic.xls char.lst


  16,   // the total messages of a language
   6,   // the total number of languages

// The offsets of languages
   7, 183, 268, 375, 593, 789, 985,

// English message offsets
  17,  24,  26,  29,  36,  43,  49,  65,  77,  93, 110, 122, 137, 153, 160, 165, 176,

// English messages
  69, 110, 103, 108, 105, 115, 104,
 199, 210,
 260, 229, 244,
  69, 115, 112,  97, 162, 111, 108,
 170, 191, 189, 189, 182, 180, 181,
  80, 111, 108, 115, 107, 105,
  67,  72,  69,  67,  75,  73,  78,  71,  32,  86,  73,  83,  73,  84,  79,  82,
  77,  69,  78,  85,  32,  83,  69,  84,  84,  73,  78,  71,
  69,  76,  69,  67,  84,  82,  79,  78,  73,  67,  32,  65,  76,  66,  85,  77,
  68,  69,  76,  69,  84,  69,  32,  84,  72,  73,  83,  32,  70,  73,  76,  69,  63,
  84,  73,  77,  69,  32,  83,  69,  84,  84,  73,  78,  71,
  68,  73,  83,  80,  76,  65,  89,  32,  83,  69,  84,  84,  73,  78,  71,
  76,  65,  78,  71,  85,  65,  71,  69,  32,  83,  69,  84,  84,  73,  78,  71,
  83,  69,  84,  84,  73,  78,  71,
  77,  79,  86,  73,  69,
  83,  84,  73,  76,  76,  32,  73,  77,  65,  71,  69,

//...
```
- The above is a C included file listing character indexes of messages for
  each language.
- The 69, 110, 103, 108, 105, 115, 104 is the character indexes of **English**.
- The 199, 210 is the character indexes of **中文**.
- See file *mlang.c* (in bin/c_src folder) for details.


## Command Line ##
### Top level ###
```
usage: langconv.exe [-h] [-v] {trans_dic,lang_id,msg_id,verify,pack} ...

positional arguments:
  {trans_dic,lang_id,msg_id,verify,pack}
                        commands
    trans_dic           Translate/Fill an Excel dictionary file.
    lang_id             Generate a C header file of language ID enumeration.
    msg_id              Generate a C header file of message ID enumeration.
    verify              Generate a report file that lists used-but-not-listed
                        characters and listed-but-not-used characters.
    pack                Generate a C included file listing an array that packs
                        multilanguage messages.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
```

### trans_dic command ###
```
usage: langconv.exe trans_dic [-h] [-o <XLS-file>] XLS-file

positional arguments:
  XLS-file              An empty Excel dictionary file to translate.

optional arguments:
  -h, --help            show this help message and exit
  -o <XLS-file>, --output <XLS-file>
                        place the output into <XLS-file>, an Excel file
                        (default "dic_trans.xls").
```

### lang_id command ###
```
usage: langconv.exe lang_id [-h] [-o <file>] XLS-file

positional arguments:
  XLS-file              An Excel dictionary file for multilanguage
                        translation.

optional arguments:
  -h, --help            show this help message and exit
  -o <file>, --output <file>
                        place the output into <file>, a C header file (default
                        "LangID.h").
```

### msg_id command ###
```
usage: langconv.exe msg_id [-h] [-o <file>] XLS-file

positional arguments:
  XLS-file              An Excel dictionary file for multilanguage
                        translation.

optional arguments:
  -h, --help            show this help message and exit
  -o <file>, --output <file>
                        place the output into <file>, a C header file (default
                        "MsgID.h").
```

### verify command ###
```
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
```

### pack command ###
```
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
```
