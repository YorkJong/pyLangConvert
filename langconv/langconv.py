# -*- coding: utf-8 -*-
"""
The purpose of this tool is for generating multi-language relative files. With
an Excel dictionary file, it can enumerate language IDs and message IDs with
the format of C header files. With an additional character list file, it can
help us indexing characters and packing messages.
"""
__software__ = "Multi-language converting tool"
__version__ = "1.05"
__author__ = "Jiang Yu-Kuan <yukuan.jiang@gmail.com>"
__date__ = "2012/11/27 (initial version) ~ 2015/03/21 (last revision)"

import os
import sys
import re
import argparse
from itertools import izip, islice, ifilterfalse, takewhile

import xlrd


#-----------------------------------------------------------------------------

def save_utf8_file(fn, lines):
    """Save string lines into an UTF8 text files.
    """
    out_file = open(fn, "w")
    out_file.write("\n".join(lines).encode("utf-8"))
    out_file.close()


def save_utf16_file(fn, lines):
    """Save string lines into an UTF16 text files.
    """
    out_file = open(fn, "wb")
    out_file.write("\r\n".join(lines).encode("utf-16"))
    out_file.close()


def read_unicode(fn):
    """Read an Unicode file that may encode with utf_16_le, utf_16_be, or utf_8.
    """
    from codecs import BOM_UTF16_LE, BOM_UTF16_BE, BOM_UTF8

    in_file = open(fn, "rb")
    bs = in_file.read()
    in_file.close()

    if  bs.startswith(BOM_UTF16_LE):
        us = bs.decode("utf_16_le").lstrip(BOM_UTF16_LE.decode("utf_16_le"))
    elif  bs.startswith(BOM_UTF16_BE):
        us = bs.decode("utf_16_be").lstrip(BOM_UTF16_BE.decode("utf_16_be"))
    else:
        us = bs.decode("utf_8").lstrip(BOM_UTF8.decode("utf_8"))

    return us


#-----------------------------------------------------------------------------

def read_xls(fn='dic.xls'):
    """Read an Excel file and return rows.
    This function will remove empty rows, empty columns, comment rows, and
    comment columns. A comment row/col is prefixing with a letter 'x' or 'X'.
    """
    def is_all_empty(seq):
        for v in seq:
            if v is not u'':
                return False
        return True

    def is_comment_line(seq):
        for v in seq:
            if v not in (u'', u'x', u'X'):
                return False
        return True

    sheet = xlrd.open_workbook(fn).sheet_by_index(0)
    rows = (sheet.row_values(y) for y in xrange(sheet.nrows))
    rows = ([unicode(v).strip() for v in vals] for vals in rows)

    # Remove empty rows and empty columns
    rows = ifilterfalse(is_all_empty, rows)
    cols = ifilterfalse(is_all_empty, izip(*rows))

    cols = list(cols)
    comment_col = list(islice(takewhile(is_comment_line, cols), 0, None))
    has_comment_col = bool(comment_col)

    rows = zip(*cols)
    comment_row = list(islice(takewhile(is_comment_line, rows), 0, None))
    has_comment_row = bool(comment_row)

    # Remove comment rows and comment columns
    if has_comment_col:
        rows = (vals[1:] for vals in rows if vals[0] not in ('x', 'X'))
    if has_comment_row:
        cols = (vals[1:] for vals in izip(*rows) if vals[0] not in ('x', 'X'))
        rows = izip(*cols)

    # Remove empty rows and empty columns (after removing comments)
    rows = ifilterfalse(is_all_empty, rows)
    cols = ifilterfalse(is_all_empty, izip(*rows))
    rows = izip(*cols)

    return list(rows)


def read_char_lst(fn):
    """Return char:index items from a given char list file.
    """
    lines = read_unicode(fn).splitlines()
    lines = (x.rstrip() for x in lines)
    lines = (x for x in lines if len(x) > 0 and not x.startswith('#'))
    idx = 0
    dic = {}
    for line in lines:
        if line.startswith(':'):
            offset = eval(line[1:])
            if str(offset).isdigit():
                idx = offset
        else:
            idxes = range(idx, idx + len(line))
            dic.update(zip(line, idxes))
            idx += len(line)
    return dic


#-----------------------------------------------------------------------------

def cumsum(X):
    """Return a list of cumulative sum for a given number list.

    Example
    -------
    >>> cumsum([0, 1, 2, 3])
    [0, 1, 3, 6]
    """
    Y = []
    y = 0
    for x in X:
        y += x
        Y += [y]
    return Y


def seq_divide(sequence, modulus):
    """Divide a sequence into multiple sub-sequences.
    >>> seq_divide('abcdefghijklmnopqr', 4)
    ['abcd', 'efgh', 'ijkl', 'mnop', 'qr']
    """
    return [sequence[i:i + modulus] for i in xrange(0, len(sequence), modulus)]


def main_basename(path):
    """Return a main name of a basename of a given file path.

    Example
    -------
    >>> main_basename('c:\code\langconv\MsgID.h')
    'MsgID.h'
    """
    base = os.path.basename(path)
    base_main, base_ext = os.path.splitext(base)
    return base_main


def replace_chars(text, replaced_pairs='', deleted_chars=''):
    """Return a char replaced text.

    Arguments
    ---------
    text -- the text
    replaced_pairs -- the replaced chars

    Example
    -------
    >>> replaced = [('a','b'), ('c','d')]
    >>> removed = 'e'
    >>> replace_chars('abcde', replaced, removed)
    'bbdd'
    """
    for old, new in replaced_pairs:
        text = text.replace(old, new)
    for ch in deleted_chars:
        text = text.replace(ch, '')
    return text


def camel_case(string):
    """Return camel case string from a space-separated string.

    Example
    -------
    >>> camel_case('good job')
    'GoodJob'
    """
    return ''.join(w.capitalize() for w in string.split())


def replace_punctuations(text):
    """Replace punctuation characters with abbreviations for a string.
    """
    punctuations = [
        ('?', 'Q'),   # Q:  question mark
        ('.', 'P'),   # P:  period; full stop
        ('!', 'E'),   # E:  exclamation mark
        ("'", 'SQ'),  # SQ: single quotation mark; single quote
        ('"', 'DQ'),  # DQ: double quotation mark; double quotes
        ('(', 'LP'),  # LP: left parenthese
        (')', 'RP'),  # RP: right parenthese
        (':', 'Cn'),  # Cn: colon
        (',', 'Ca'),  # Ca: comma
        (';', 'S'),   # S:  semicolon
    ]
    deleted = '+-*/^=%$#@|\\<>{}[]'
    return replace_chars(text, punctuations, deleted)


def remain_alnum(text):
    """Remain digits and English letters of a string.
    """
    return ''.join(c for c in text if c.isalnum()
                                   and ord(' ') <= ord(c) <= ord('z'))


def array_str_from_ints(ints):
    """Return the string of a C integer array from an integer list

    Example
    -------
    >>> array_str_from_ints([1, 2, 3])
    '1, 2, 3'
    """
    return '%4d,' * len(ints) % tuple(ints)


#-----------------------------------------------------------------------------

def prefix_authorship(lines, comment_mark='#'):
    """Prefix authorship infomation to the given lines
    with given comment-mark.
    """
    prefix = ['%s Generated by the %s v%s' % (comment_mark,
              __software__, __version__)]
    prefix += ['%s    !author: %s' % (comment_mark, __author__)]
    prefix += ['%s    !trail: %s %s' % (comment_mark,
               os.path.basename(sys.argv[0]), ' '.join(sys.argv[1:]))]
    return prefix + lines


def wrap_header_guard(lines, h_fn):
    """Wrap a C header guard for a given line list.
    """
    def underscore(txt):
        """Return an under_scores text from a CamelCase text.

        This function will leave a CamelCase text unchanged.
        """
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', txt)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    h_fn_sig = '_%s_H' % underscore(main_basename(h_fn)).upper()
    begin = ['#ifndef %s' % h_fn_sig]
    begin += ['#define %s' % h_fn_sig, '', '']
    end = ['', '', '#endif // %s' % h_fn_sig, '']
    return begin + lines + end


def c_identifier(text):
    """Convert input text into an legal identifier in C.

    Example
    -------
    >>> c_identifier("Hello World")
    'HelloWorld'
    >>> c_identifier("Anti-Shake")
    'Antishake'
    """
    if ' ' in text:
        text = camel_case(text)
    text = re.sub(r'\+\d+', lambda x: x.group().replace('+', 'P'), text)
    text = re.sub(r'\-\d+', lambda x: x.group().replace('-', 'N'), text)
    text = replace_punctuations(text)
    return remain_alnum(text)


#-----------------------------------------------------------------------------

def get_lang_names(rows):
    """
    Get language names
    """
    heads = rows[0]
    return [h for h in heads if h.upper() != 'ID']


def gen_mlang_tbl(rows):
    """Generate the multilanguage message table.
    """
    heads = (h.upper() for h in rows[0])
    cols = izip(*rows[1:])
    return dict(izip(heads, cols))


def gen_msg_ids(rows):
    """ Generate and return message IDs.
    """
    tbl = gen_mlang_tbl(rows)
    ids = (id or msg for id, msg in zip(tbl['ID'], tbl['ENGLISH']))
    return [c_identifier(id) for id in ids]


def offsets_from_lens(lens):
    """Returns an offset list from a length list.

    Example
    -------
    >>> offsets_from_lens([1, 2, 3])
    [4, 5, 7, 10]
    """
    return [x + len(lens) + 1 for x in cumsum([0, ] + lens)]

#-----------------------------------------------------------------------------

def gen_lang_id_hfile(rows, h_fn):
    """Generate a C header file of language ID enumeration.
    """
    lines = ['/** Language Indexes */']
    lines += ['typedef enum {']
    lines += ['    L_%s,' % lang for lang in get_lang_names(rows)]
    lines += ['    L_End,']
    lines += ['    L_Total = L_End']
    lines += ['} Lang;']

    lines = wrap_header_guard(lines, h_fn)
    lines = prefix_authorship(lines, comment_mark='//')
    save_utf8_file(h_fn, lines)


def gen_msg_id_hfile(rows, h_fn):
    """Generate a C header file of message ID enumeration.
    """
    lines = ['/** IDs of Messages */']
    lines += ["typedef enum {"]
    lines += ['    MSG_%s,' % id for id in gen_msg_ids(rows)]
    lines += ['    MSG_End,']
    lines += ['    MSG_Total = MSG_End']
    lines += ['} MsgID;']

    lines = wrap_header_guard(lines, h_fn)
    lines = prefix_authorship(lines, comment_mark='//')
    save_utf8_file(h_fn, lines)


def verify(rows, char_tbl, report_fn):
    """Generate a report file to list used-but-not-listed characters and
    listed-but-not-used characters.
    """
    def get_mlang_records(rows):
        """Get records without ID column
        """
        heads, records = rows[0], rows[1:]
        heads = [h.upper() for h in heads]
        i = heads.index('ID')
        return [r[:i] + r[i+1:] for r in records]

    char_use = set([])
    for r in get_mlang_records(rows):
        char_use |= set(''.join(r))

    char_lst = set(char_tbl)
    char_not_lst = sorted(char_use - char_lst)
    char_not_use = sorted(char_lst - char_use)

    lines = []
    if char_not_lst != []:
        lines += ['', '# Chars used but not listed:']
        lines += seq_divide(''.join(char_not_lst), 10)
    if char_not_use != []:
        lines += ['', '# Chars listed but not used:']
        lines += seq_divide(''.join(char_not_use), 10)

    lines = prefix_authorship(lines, comment_mark='#')
    save_utf16_file(report_fn, lines)


def pack(rows, char_tbl, h_fn):
    """Generate a C included file listing an array that packs multilanguage
    messages.

    The Output Format
    -----------------
    MLangHeader LangMsg^L
        L: the total number of languages
    MLangHeader: MsgCounterPerLang LangCount LangOffset^(L+1)
    LangMsg: MsgOffset^(M+1) Msg^M
        M: the total number of messages
    """
    def lang_offsets(langs, mlang_tbl):
        """Return language offsets.
        """
        msg_total = len(mlang_tbl['ID'])
        langs = [lang.upper() for lang in langs]
        lens = [msg_total+1+len(''.join(mlang_tbl[lang])) for lang in langs]
        return offsets_from_lens(lens)

    def msg_offsets(msgs):
        """Return message offsets.
        """
        return offsets_from_lens([len(x) for x in msgs])

    def char_idx_str_from_msg(msg, char_tbl):
        """Generate the string of indexes of chars in a message.
        """
        return array_str_from_ints([char_tbl[c] for c in msg])

    langs = get_lang_names(rows)
    mlang_tbl = gen_mlang_tbl(rows)

    lines = [''] * 2
    lines += ['%4d,   // the total messages of a language'
                % len(mlang_tbl['ID'])]
    lines += ['%4d,   // the total number of languages' % len(langs)]
    lines += ['', '// The offsets of languages']
    lines += [array_str_from_ints(lang_offsets(langs, mlang_tbl))]
    for lang in langs:
        msgs = mlang_tbl[lang.upper()]
        lines += ['', '// %s message offsets' % lang]
        lines += [array_str_from_ints(msg_offsets(msgs))]
        lines += ['', '// %s messages' % lang]
        lines += [char_idx_str_from_msg(m, char_tbl) for m in msgs]

    lines = prefix_authorship(lines, comment_mark='//')
    save_utf8_file(h_fn, lines)


#-----------------------------------------------------------------------------

def parse_args(args):
    # create top-level parser
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--version', action='version',
                        version='%s v%s by %s' %
                        (__software__, __version__, __author__))
    subparsers = parser.add_subparsers(help='commands')

    #--------------------------------------------------------------------------

    # create the parent parser of XLS-file
    xls = argparse.ArgumentParser(add_help=False)
    xls.add_argument('rows', metavar='XLS-file', type=read_xls,
        help='An Excel dictionary file for multilanguage translation.')

    # create the parser for the "lang_id" command
    sub = subparsers.add_parser('lang_id', parents=[xls],
        help='Generate a C header file of language ID enumeration.')
    sub.set_defaults(func=gen_lang_id_hfile, outfile='LangID.h')
    sub.add_argument('-o', '--output', metavar='<file>', dest='outfile',
        help='''place the output into <file>, a C header file (default "%s").
            ''' % sub.get_default('outfile'))

    # create the parser for the "msg_id" command
    sub = subparsers.add_parser('msg_id', parents=[xls],
        help='Generate a C header file of message ID enumeration.')
    sub.set_defaults(func=gen_msg_id_hfile, outfile='MsgID.h')
    sub.add_argument('-o', '--output', metavar='<file>', dest='outfile',
        help='''place the output into <file>, a C header file (default "%s").
            ''' % sub.get_default('outfile'))

    #--------------------------------------------------------------------------

    # create the parent parser of char list file
    lst = argparse.ArgumentParser(add_help=False)
    lst.add_argument('char_tbl', metavar='LST-file', type=read_char_lst,
        help='An unicode text file that lists unicode characters.')

    # create the parser for the "verify" command
    sub = subparsers.add_parser('verify', parents=[xls, lst],
        help='''Generate a report file that lists used-but-not-listed
            characters and listed-but-not-used characters.''')
    sub.set_defaults(func=verify, outfile='verify.report')
    sub.add_argument('-o', '--output', metavar='<file>', dest='outfile',
        help='''place the output into <file>, an unicode text file
            (default "%s").
            ''' % sub.get_default('outfile'))

    # create the parser for the "pack" command
    sub = subparsers.add_parser('pack', parents=[xls, lst],
        help='''Generate a C included file listing an array that packs
            multilanguage messages.''')
    sub.set_defaults(func=pack, outfile='mlang.i')
    sub.add_argument('-o', '--output', metavar='<file>', dest='outfile',
        help='''place the output into <file>, a C included file
            (default "%s").
            ''' % sub.get_default('outfile'))

    #--------------------------------------------------------------------------

    # parse args and execute functions
    args = parser.parse_args(args)
    if 'char_tbl' in args:
        args.func(args.rows, args.char_tbl, args.outfile)
    else:
        args.func(args.rows, args.outfile)


def main():
    """Start point of this module.
    """
    try:
        parse_args(sys.argv[1:])
    except IOError as err:
        print err
    except ValueError as err:
        print err


if __name__ == '__main__':
    main()
    #rows = read_xls()
    #gen_lang_id_hfile(rows, 'LangID.h')
    #gen_msg_id_hfile(rows, 'MsgID.h')
    #char_tbl = read_char_lst('char.lst')
    #verify(rows, char_tbl, 'verify.report')
    #pack(rows, char_tbl, 'mlang.i')
