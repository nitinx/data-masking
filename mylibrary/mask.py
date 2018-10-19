# 04 May 2018 | Masking Routines Library

"""Masking Routines Library
Library that:
1. Masks strings by Character Substitution - Random
2. Masks strings by Character Substitution - Deterministic
3. Masks strings by Character Shuffling - Random
4. Masks strings by Character Shuffling - Deterministic
"""

import logging
import random
import string

log = logging.getLogger(__name__)


class Mask:

    def substitution_char(self, value_org):
        """Random Character Substitution"""
        log.debug("substitution_char() | <START>")

        data_set = string.ascii_uppercase + string.digits + string.ascii_lowercase
        value_msk = ''.join(random.choice(data_set) for x in range(len(value_org)))

        log.debug("substitution_char() | <END>")
        return value_msk

    def substitution_char_det(self, value_org):
        """Deterministic Character Substitution"""
        log.debug("substitution_char_det() | <START>")

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

        log.debug(value_org + ' --> ' + value_msk)
        log.debug("substitution_char_det() | <END>")
        return value_msk

    def shuffle(self, value_org):
        """Random Shuffle"""
        log.debug("shuffle_random() | <START>")

        shuffle_list = list(str(value_org))
        random.shuffle(shuffle_list)
        value_msk = ''.join(shuffle_list)

        log.debug(str(value_org) + ' --> ' + value_msk)
        log.debug("shuffle_random() | <END>")
        return value_msk

    def shuffle_det(self, value_org):
        """Deterministic Shuffle"""
        log.debug("shuffle_det() | <START>")

        shuffle_list = list(str(value_org))
        random.Random(4).shuffle(shuffle_list)
        value_msk = ''.join(shuffle_list)

        log.debug(str(value_org) + ' --> ' + value_msk)
        log.debug("shuffle_det() | <END>")
        return value_msk
