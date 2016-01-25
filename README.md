# LangConvert #

LangConvert is an open source Python application to generate multi-language
relative files for application on embedded systems. With an Excel dictionary
file, it can enumerate language IDs and message IDs with the format of C header
files. With an additional character list file, it can help us indexing
characters and packing messages.


## Install ##

1. Download a binary distribution of PicCrop (e.g., *LangConvert-1.05-bin.zip*)
   from [Downloads](https://bitbucket.org/YorkJong/pylangconvert/downloads) page.
2. Uncompress the binary distribution.


## Getting Started ##

1. Install LangConvert.
2. Edit the *dic.xls*
3. Edit the *char.lst* or just create an empty *char.lst*
4. Run the `demo.bat`
    * This will generate *LangID.h*, *MsgID.h*, *malng.i* in c_src directory
    * And generate *verify.report*
5. Refined *char.lst* according the *verify.report*

### Note ###
* Run `clean.bat` to remove the generated files


## Command Line ##
### Top level ###
```
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
