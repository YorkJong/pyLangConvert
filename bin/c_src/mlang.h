/**
 * @file mlang.h
 *      for unpacking multi-language messages
 * @author Jiang Yu-Kuan, yukuan.jiang@gmail.com
 * @version 1.0
 * @date 2012/12/03 (initial version)
 * @date 2012/12/03 (last revision)
 */

#ifndef __MLANG_H
#define __MLANG_H

#include <stdint.h>
#include <stdlib.h>

#include "LangID.h"
#include "MsgID.h"

typedef uint16_t Char;

void ML_setLang(Lang);
void ML_getMsgStr(MsgID, Char**, size_t* len);


#endif
