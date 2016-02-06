# -*- coding: utf-8 -*-
"""
This tool is for shaping Arabic text, applying them with operations of
normalizing, mark combining, cursive joining, ligature joining,
bidirection reordering, and mirror char correcting.
"""
__software__ = "Arabic Shaping tool"
__version__ = "1.02"
__author__ = "Jiang Yu-Kuan <yukuan.jiang@gmail.com>"
__date__ = "2012/05/04 (initial version); 2012/05/18 (last revision)"

import unicodedata
import re
from itertools import islice


#------------------------------------------------------------------------------
# Common Help functions
#------------------------------------------------------------------------------

def partition(text, seps):
    """Partite a text with separators listed in seps.

    Example
    -------
    >>> partition(u'abc:;de;fg;', u':;')
    [u'abc', u':', u';', u'de', u';', u'fg', u';']
    """
    pattern = re.compile(u'[%s]|[^%s]+' % (seps, seps))
    return pattern.findall(text)


def is_arabic(x):
    return u'\u0600' <= x <= u'\u06ff'

#------------------------------------------------------------------------------
# Tables of Arabic Glyph Types
#------------------------------------------------------------------------------

# ref. http://en.wikipedia.org/wiki/Template:Arabic_alphabet_shapes/joining
# ref. Arabic Presentation Forms-B
# ref. Arabic Presentation Forms-A

RIGHT_JOINING_GLYPH_TABLE = {
    # X:          Xn         Xr
    # char:     isolated   final
    u'\u0622': (u'\ufe81', u'\ufe82'),
    u'\u0623': (u'\ufe83', u'\ufe84'),
    u'\u0624': (u'\ufe85', u'\ufe86'),
    u'\u0625': (u'\ufe87', u'\ufe88'),
    u'\u0627': (u'\ufe8d', u'\ufe8e'),
    u'\u0629': (u'\ufe93', u'\ufe94'),
    u'\u062f': (u'\ufea9', u'\ufeaa'),
    u'\u0630': (u'\ufeab', u'\ufeac'),
    u'\u0631': (u'\ufead', u'\ufeae'),
    u'\u0632': (u'\ufeaf', u'\ufeb0'),
    u'\u0648': (u'\ufeed', u'\ufeee'),

    # for combined by combine function
    # X:          Xn         Xr
    u'\u076c': (u'\u076c', u'\u076c'),
    u'\u0692': (u'\u0692', u'\u0692'),
    u'\u06c6': (u'\u06c6', u'\u06c6'),
    u'\u06c9': (u'\u06c9', u'\u06c9'),
    u'\u06ee': (u'\u06ee', u'\u06ee'),
    u'\u06ef': (u'\u06ef', u'\u06ef'),

    # for Persian, Urdu, Sindhi and Central Asian
    u'\u0698': (u'\ufb8a', u'\ufb8b'),  # jeh
    u'\u06c0': (u'\ufba4', u'\ufba5'),  # heh with yeh
    u'\u06d3': (u'\ufbb0', u'\ufbb1'),
}

DUAL_JOINING_GLYPH_TABLE = {
    # X:          Xn         Xr         Xl         Xm
    # char:     isolated   final      initial    medial
    u'\u0626': (u'\ufe89', u'\ufe8a', u'\ufe8b', u'\ufe8c'),
    u'\u0628': (u'\ufe8f', u'\ufe90', u'\ufe91', u'\ufe92'),
    u'\u062a': (u'\ufe95', u'\ufe96', u'\ufe97', u'\ufe98'),
    u'\u062b': (u'\ufe99', u'\ufe9a', u'\ufe9b', u'\ufe9c'),
    u'\u062c': (u'\ufe9d', u'\ufe9e', u'\ufe9f', u'\ufea0'),
    u'\u062d': (u'\ufea1', u'\ufea2', u'\ufea3', u'\ufea4'),
    u'\u062e': (u'\ufea5', u'\ufea6', u'\ufea7', u'\ufea8'),
    u'\u0633': (u'\ufeb1', u'\ufeb2', u'\ufeb3', u'\ufeb4'),
    u'\u0634': (u'\ufeb5', u'\ufeb6', u'\ufeb7', u'\ufeb8'),
    u'\u0635': (u'\ufeb9', u'\ufeba', u'\ufebb', u'\ufebc'),
    u'\u0636': (u'\ufebd', u'\ufebe', u'\ufebf', u'\ufec0'),
    u'\u0637': (u'\ufec1', u'\ufec2', u'\ufec3', u'\ufec4'),
    u'\u0638': (u'\ufec5', u'\ufec6', u'\ufec7', u'\ufec8'),
    u'\u0639': (u'\ufec9', u'\ufeca', u'\ufecb', u'\ufecc'),
    u'\u063a': (u'\ufecd', u'\ufece', u'\ufecf', u'\ufed0'),
    #u'\u063b': (u'\u0000', u'\u0000', u'\u0000', u'\u0000'),
    #u'\u063c': (u'\u0000', u'\u0000', u'\u0000', u'\u0000'),
    #u'\u063d': (u'\u0000', u'\u0000', u'\u0000', u'\u0000'),
    #u'\u063e': (u'\u0000', u'\u0000', u'\u0000', u'\u0000'),
    #u'\u063f': (u'\u0000', u'\u0000', u'\u0000', u'\u0000'),
    u'\u0641': (u'\ufed1', u'\ufed2', u'\ufed3', u'\ufed4'),
    u'\u0642': (u'\ufed5', u'\ufed6', u'\ufed7', u'\ufed8'),
    u'\u0643': (u'\ufed9', u'\ufeda', u'\ufedb', u'\ufedc'),
    u'\u0644': (u'\ufedd', u'\ufede', u'\ufedf', u'\ufee0'),
    u'\u0645': (u'\ufee1', u'\ufee2', u'\ufee3', u'\ufee4'),
    u'\u0646': (u'\ufee5', u'\ufee6', u'\ufee7', u'\ufee8'),
    u'\u0647': (u'\ufee9', u'\ufeea', u'\ufeeb', u'\ufeec'),
    u'\u0649': (u'\ufeef', u'\ufef0', u'\ufbe8', u'\ufbe9'),
    u'\u064a': (u'\ufef1', u'\ufef2', u'\ufef3', u'\ufef4'),

    # for combined by combine function
    # X:          Xn         Xr                 Xl              Xm
    u'\u0681': (u'\u0681', u'\ufea2\u0654', u'\ufea3\u0654', u'\ufea4\u0654'),
    u'\u06b5': (u'\u06b5', u'\u06b5', u'\ufedf\u065a', u'\ufee0\u065a'),
    u'\u06ce': (u'\u06ce', u'\ufef0\u065a', u'\ufbe8\u065a', u'\ufbe9\u065a'),
    u'\u077e': (u'\u077e', u'\u077e', u'\ufeb3\u065a', u'\ufeb4\u065a'),

    # for combined after NFKC
    u'\u06c2': (u'\u06c2', u'\ufba7\u0654', u'\ufba7\u0654', u'\ufba7\u0654'),

    # for Persian, Urdu, Sindhi and Central Asian
    # X:          Xn         Xr         Xl         Xm
    u'\u067e': (u'\ufb56', u'\ufb57', u'\ufb58', u'\ufb59'),  # peh
    u'\u0686': (u'\ufb7a', u'\ufb7b', u'\ufb7c', u'\ufb7d'),  # cheh
    u'\u06a9': (u'\ufb8e', u'\ufb8f', u'\ufb90', u'\ufb91'),  # KEHEH
    u'\u06af': (u'\ufb92', u'\ufb93', u'\ufb94', u'\ufb95'),  # gaf
    u'\u06c1': (u'\ufba6', u'\ufba7', u'\ufba8', u'\ufba9'),
    u'\u06cc': (u'\ufbfc', u'\ufbfd', u'\ufbfe', u'\ufbff'),  # FARSI YEH
}


#------------------------------------------------------------------------------
# Querying functions of joing types
#------------------------------------------------------------------------------

def is_transparent(unichar):
    """Decide if the joining type of an Unicode char is transparent.

    ref. Unicode Standard 6.1, Table 8-3. Primary Arabic Joining Types
    """
    CF_NONJOINING_CHARS = (
        u'\u0600',  # ARABIC NUMBER SIGN
        u'\u0601',  # ARABIC SIGN SANAH
        u'\u0602',  # ARABIC FOOTNOTE MARKER
        u'\u0603',  # ARABIC SIGN SAFHA
        u'\u06DD',  # ARABIC END OF AYAH
    )
    if unicodedata.combining(unichar):
        return True
    if unichar in CF_NONJOINING_CHARS:
        return False
    if unicodedata.category(unichar) == 'Cf':
        return True
    return False


def is_causing(unichar):
    """Decide if the joining type of an Unicode char is join-causing.

    ref. DerivedJoiningType.txt
    """
    CAUSING_CHARS = (
        u'\u0640',  # Lm    ARABIC TATWEEL
        u'\u07FA',  # Lm    NKO LAJANYALAN
        u'\u200D',  # Cf    ZERO WIDTH JOINER
    )
    return unichar in CAUSING_CHARS


def is_right(unichar):
    """Decide if the joining type of an Unicode char is right-joining.

    ref. DerivedJoiningType.txt
    """
    return unichar in RIGHT_JOINING_GLYPH_TABLE


def is_dual(unichar):
    """Decide if the joining type of an Unicode char is dual-joining.

    ref. DerivedJoiningType.txt
    """
    return unichar in DUAL_JOINING_GLYPH_TABLE


#------------------------------------------------------------------------------

def is_right_causing(unichar):
    """Decide if an Unicode character is right join-causing.
    """
    return is_dual(unichar) or is_causing(unichar)


def is_left_causing(unichar):
    """Decide if an Unicode character is left join-causing.
    """
    return is_dual(unichar) or is_right(unichar) or is_causing(unichar)


#------------------------------------------------------------------------------
# Shaping functions
#------------------------------------------------------------------------------

def combine(unistr):
    """Combine the Arabic combining characters those are not handled by the
    Unicode normalization process and exist corresponding combined character.

    This function here is for a string with *memory representation order*.

    References
    ----------
    - List of All Arabic Script Combining Marks

    Examples
    --------
    >>> combine(u'\u0649\u0654')
    u'\u0626'
    >>> combine(u'\uFEE0\uFE8E\u0647\u0654\uFEDF\uFE8E')
    u'\ufee0\ufe8e\u06c0\ufedf\ufe8e'
    """
    pairs = (
        (u'\u0649\u0654', u'\u0626'),   # D 4 glyphs
        #(u'\u06cc\u0654', u'\u0626'),  # R 2 glyphs; non-support
        (u'\u0647\u0654', u'\u06c0'),   # R 2 glyphs
        #(u'\u0647\u0654', u'\u06c2'),   # R 2 glyphs; Ambiguity
        (u'\u062d\u0654', u'\u0681'),   # D
        (u'\u0631\u0654', u'\u076c'),   # R
        (u'\u0631\u065a', u'\u0692'),   # R
        (u'\u0644\u065a', u'\u06b5'),   # D
        (u'\u0648\u065a', u'\u06c6'),   # R
        (u'\u0649\u065a', u'\u06ce'),   # D
        (u'\u06cc\u065a', u'\u06ce'),   # D
        (u'\u0633\u065b', u'\u077e'),   # D
        (u'\u0648\u065b', u'\u06c9'),   # R
        (u'\u062f\u065b', u'\u06ee'),   # R
        (u'\u0631\u065b', u'\u06ef'),   # R
    )
    for seq, combined in pairs:
        unistr = unistr.replace(seq, combined)
    return unistr


def join(unistr):
    """Apply Arabic cursive-joining behavior to a given Unicode string.

    Each Unicode character has a joining type, i.e. right, left (none),
    dual (left&right), causing, non-joining or transparent.

    Transparent type applies to all combining marks and format marks.

    Derived Arabic joining types are as follows:

        Right join-causing: dual (+ left) + causing
        Left join-causing: dual + right + causing

    Symbol Definitions:

        C_T: a transparent character
        C_R: a right joining character
        C_L: a left joining character (no left joining characters in Unicode)
        C_D: a dual joining character
        C_CR: a right join-causing character
        C_CL: a left join-causing character

        Xn: nominal glyph
        Xr: right-joining glyph form
        Xl: left-joining glyph form
        Xm: dual-joining (medial) glyph form)

    Rules are as follows (for a string *memory representation order*):

        R1: Transparent characters (C_T) do not affect joining behavior
        R2: C_CR + C_R -> C_CR + Xr
        R3: C_L + C_CL -> Xl + C_CL -- meaningless
        R4: C_CR + C_D + C_CL -> C_CR + Xm + C_CL
        R5: C_CR + C_D -> C_CR + Xr
        R6: C_D + C_CL -> Xl + C_CL
        R7: Otherwise the character will get form Xn

    References
    ----------
    - Unicode Standard 6.1, Section "Arabic Cursive Joining"
    - http://en.wikipedia.org/wiki/Template:Arabic_alphabet_shapes/joining
    - Arabic Presentation Forms-B
    - Arabic Presentation Forms-A

    Examples
    --------
    >>> join(u'\u0644\u0651\u0645') # R1
    u'\ufedf\u0651\ufee2'
    >>> join(u'\u0640\u0627')       # R2
    u'\u0640\ufe8e'
    >>> join(u'\u0640\u0645\u0640') # R4
    u'\u0640\ufee4\u0640'
    >>> join(u'\u0640\u0645')       # R5
    u'\u0640\ufee2'
    >>> join(u'\u0645\u0640')       # R6
    u'\ufee3\u0640'
    >>> join(u'\u0627\u0640')       # R7
    u'\ufe8d\u0640'
    """
    chars = list(unistr)
    prev = now = post = 0
    ch_prev = chars[0]
    for now, ch_now in enumerate(chars):
        if not is_arabic(ch_now) or is_transparent(ch_now):
            continue

        if is_right(ch_now):
            xn, xr = RIGHT_JOINING_GLYPH_TABLE[ch_now]
            xl = xm = xn            # R7
        elif is_dual(ch_now):
            xn, xr, xl, xm = DUAL_JOINING_GLYPH_TABLE[ch_now]
        else:
            continue

        post = now
        for post, ch_post in enumerate(islice(chars,
                                              now + 1, len(chars)), now + 1):
            if not is_transparent(ch_post):
                break               # R1

        to_right = to_left = False
        if prev < now:
            to_right = is_right_causing(ch_prev)
        if now < post:
            to_left = is_left_causing(ch_post)
        prev, ch_prev = now, ch_now

        if to_right and to_left:    # R4
            chars[now] = xm
        elif to_right:              # R2, R5
            chars[now] = xr
        elif to_left:               # (R3,) R6
            chars[now] = xl
        else:                       # R7
            chars[now] = xn

    return ''.join(chars)


def ligature(unistr):
    """Apply obligatory Arabic ligature substitution to a given Unicode string.

    Rules are as follows (for a string *memory representation order*):

        L1: Transparent characters do not affect the ligating behavior
        L2: LAMm + ALEFr -> (LAM-ALEF)r
        L3: LAMl + ALEFr -> (LAM-ALEF)n

    References
    ----------
    - Unicode Standard 6.1, Section "Arabic Ligatures"

    Examples
    --------
    >>> ligature(u'\uFEE0\uFE8E')
    u'\ufefc'
    >>> ligature(u'\uFEDF\u0653\uFE8E')
    u'\ufefb\u0653'
    """
    def are_trans(unichars):
        """Decide if characters listed in unichars are all transparent.
        """
        return all(is_transparent(c) for c in unichars)

    # L1: skip over transparent characters

    lams = u'\uFEE0\uFEDF'
    alefs = u'\uFE8E\uFE88\uFE84\uFE82'
    seq = partition(unistr, lams + alefs)
    i = 0
    while i < len(seq):
        if seq[i] in lams and are_trans(seq[i + 1]) and seq[i + 2] in alefs:
            seq[i + 1], seq[i + 2] = seq[i + 2], seq[i + 1]
            i += 2
        i += 1
    unistr = ''.join(seq)

    # L2: LAMm + ALEFr -> (LAM-ALEF)r
    # L3: LAMl + ALEFr -> (LAM-ALEF)n

    pairs = (
        (u'\uFEE0\uFE8E', u'\uFEFC'),   # L2; (LAM-ALEF)r
        (u'\uFEDF\uFE8E', u'\uFEFB'),   # L3; (LAM-ALEF)n
        (u'\uFEE0\uFE88', u'\uFEFA'),   # L2; (LAM-ALEF)r with Hamza below
        (u'\uFEDF\uFE88', u'\uFEF9'),   # L3; (LAM-ALEF)n with Hamza below
        (u'\uFEE0\uFE84', u'\uFEF8'),   # L2; (LAM-ALEF)r with Hamza above
        (u'\uFEDF\uFE84', u'\uFEF7'),   # L3; (LAM-ALEF)n with Hamza above
        (u'\uFEE0\uFE82', u'\uFEF6'),   # L2; (LAM-ALEF)r with Madda above
        (u'\uFEDF\uFE82', u'\uFEF5'),   # L3; (LAM-ALEF)n with Madda above
    )

    for seq, lig in pairs:
        unistr = unistr.replace(seq, lig)

    return unistr


def reorder(unistr):
    """Reorder the memory representation for display because the Arabic script
    is written from right to left.

    References
    ----------
    - Unicode Standard Annex #9, Unicode Bidirectional Algorithm

    Examples
    --------
    >>> reorder(u'\u0660\u0661\u0662')
    u'\u0660\u0661\u0662'
    >>> reorder(u'\uFEE0\uFE8E')
    u'\ufe8e\ufee0'
    >>> reorder(u'\uFEE0\uFE8E\u0660\u0661\u0662\uFEDF\uFE8E')
    u'\ufe8e\ufedf\u0660\u0661\u0662\ufe8e\ufee0'
    >>> reorder(u'Hollo, Arabic')
    u'Hollo, Arabic'
    >>> reorder(u'\uFEE0\uFE8E Hollo, Arabic \uFEDF\uFE8E')
    u'\ufe8e\ufedf Hollo, Arabic \ufe8e\ufee0'
    >>> reorder(u'\u0627\u0653')
    u'\u0627\u0653'
    >>> reorder(u'\uFEE0\uFE8E\u0627\u0653\uFEDF\uFE8E')
    u'\ufe8e\ufedf\u0627\u0653\ufe8e\ufee0'
    >>> reorder(u'\u0645\u0651\u064e\u0646')    # D T T D
    u'\u0646\u0645\u0651\u064e'
    """
    chars = list(unistr)

    # 1. reverse none Arabic characters and digits

    rtl_chars = ''.join([
        u'\u0600-\u065F\u066A-\u06EF\u06FA-\u06FF',  # Arabic non-digits
        u'\u0750-\u077F',   # Arabic Supplement
        u'\u08A0-\u08FF',   # Arabic Extended-A
        u'\uFB50-\uFDFF',   # Arabic Presentation Forms-A
        u'\uFE70-\uFEFF',   # Arabic Presentation Forms-B
    ])
    pattern = re.compile(u'[^%s]{2,}' % rtl_chars)
    for m in pattern.finditer(unistr):
        chars[m.start():m.end()] = m.group(0)[::-1]

    # 2. reverse the Arabic characters of to be combined sequence

    # Category Mn part of Arabic characters (ref. DerivedJoiningType.txt)
    ArabicMn = u'\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06DC' \
               u'\u06DF-\u06E4\u06E7-\u06E8\u06EA-\u06ED'
    pattern = re.compile(u'[^%s][%s]+' % (ArabicMn, ArabicMn))
    for m in pattern.finditer(unistr):
        chars[m.start():m.end()] = m.group(0)[::-1]

    # 3. reverse all and join chars
    return ''.join(chars[::-1])


def mirror(unistr):
    """Replace characters with mirrored ones if those existing.

    References
    ----------
    - BidiMirroring.txt
    - Unicode Standard Annex #9, Unicode Bidirectional Algorithm

    Examples
    --------
    >>> mirror(u')abc(')
    u'(abc)'
    >>> mirror(u'a <= b; b >= c')
    u'a >= b; b <= c'
    """
    pairs = (
    #    char   mirror
        (u'(',  u')'),
        (u'[',  u']'),
        (u'{',  u'}'),
        (u'<',  u'>'),
    )

    signature = lambda ch: u'__%s__' % unichr(ord(ch) + 256)
    for char, mirr in pairs:
        unistr = unistr.replace(char, signature(mirr))
        unistr = unistr.replace(mirr, char)
        unistr = unistr.replace(signature(mirr), mirr)

    return unistr


#------------------------------------------------------------------------------

def shape(unistr):
    """Apply Arabic shaping behavior to a given Unicode string.

    Eamples
    -------
    >>> shape(u'\u0627\u0644\u0639\u0631\u0628\u064a\u0629')
    u'\ufe94\ufef4\ufe91\ufead\ufecc\ufedf\ufe8d'
    >>> unistr = u'\u0645\u0651\u064e\u0646'    # D T T D
    >>> unicodedata.normalize('NFKC', unistr)
    u'\u0645\u064e\u0651\u0646'
    >>> shape(unistr)
    u'\ufee6\ufee3\u064e\u0651'
    >>> shape('你好嗎？'.decode('utf8'))
    u'\u4f60\u597d\u55ce\uff1f'
    """
    normailized = unicodedata.normalize('NFKC', unistr)
    if any(is_arabic(c) for c in normailized):
        unistr = normailized
        unistr = combine(unistr)
        unistr = join(unistr)
        unistr = ligature(unistr)
        unistr = reorder(unistr)
        unistr = mirror(unistr)
    return unistr


#------------------------------------------------------------------------------
# Test
#------------------------------------------------------------------------------

def main():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    main()
