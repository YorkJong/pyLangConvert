/**
 * @file mlang.c
 *      for unpacking multi-language messages
 * @author Jiang Yu-Kuan, yukuan.jiang@gmail.com
 * @version 1.0
 * @date 2012/12/03 (initial version)
 * @date 2012/12/03 (last revision)
 */
#include <assert.h>

#include "mlang.h"


static const uint16_t _pack[] = {
    #include "mlang.i"
};


#define MSGS _pack[0]
#define LANGS _pack[1]
#define LANG_OFFSET (&_pack[2])


static Lang _lang;


/** Sets current language. */
void ML_setLang(Lang lang)
{
    assert (lang < LANGS);
    _lang = lang;
}


/** Gets Char string of a given message.
 * @param m message ID
 * @param str buffer of the Char string of the message
 * @param len length of the Char string
 */
void ML_getMsgStr(MsgID m, Char** str, size_t* len)
{
    const uint16_t *msgOffset = &LANG_OFFSET[LANG_OFFSET[_lang]];

    assert (m < MSGS);

    *str = (Char*)&msgOffset[msgOffset[m]];
    *len = msgOffset[m+1] - msgOffset[m];
}
