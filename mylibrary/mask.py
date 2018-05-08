# 04 May 2018 | Masking Library

import logging
import random

log = logging.getLogger(__name__)


class Mask:

    def substitution_char(self, value_org):
        """Deterministic Character Substitution"""
        log.debug("substitution_char() | <START>")

        value_msk = ''

        for i in range(len(value_org)):
            value_asc = ord(value_org[i]) + (len(value_org) - i)

            # Space or Period or @
            if value_org[i] == ' ' or value_org[i] == '.' or value_org[i] == ' ' or value_org[i] == '@' \
                or value_org[i] == '-' or value_org[i] == '(' or value_org[i] == ')':
                value_asc = ord(value_org[i])

            # A to Z
            elif 65 <= ord(value_org[i]) <= 90:
                if value_asc > 90:
                    value_asc = 65 + (value_asc - 90)

            # a to z
            elif 97 <= ord(value_org[i]) <= 122:
                if value_asc > 90:
                    value_asc = 97 + (value_asc - 122)

            # 0 to 9
            elif 48 <= ord(value_org[i]) <= 57:
                if value_asc > 57:
                    '''if (value_asc - 57) > 9:
                        value_asc = (value_asc - 57) % 9
                    else:'''
                    value_asc = 48 + (value_asc - 57)
            else:
                value_asc = ord(value_org[i]) + (len(value_org) - i)

            value_msk += chr(value_asc)

        log.info(value_org + ' --> ' + value_msk)
        log.debug("substitution_char() | <END>")
        return value_msk

    def shuffle(self, value_org):
        """Deterministic Shuffle"""
        log.debug("shuffle() | <START>")

        shuffle_list = list(value_org)
        random.Random(4).shuffle(shuffle_list)
        value_msk = ''.join(shuffle_list)

        log.debug(value_org + ' --> ' + value_msk)
        log.debug("shuffle() | <END>")
        return value_msk
