#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012-2013 Yamauchi, Hitoshi
#
# test unicode
#
"""
\file
\brief LinkVectorExtractor test: en_en (English Writer, English Author)
"""

import os
import LinkVectorExtractor
import unittest, codecs


def print_str(_str):
    """print unicode or string using utf-8 without casting exception"""
    if type(_str) == type(u'a'):
        print _str.encode('utf-8', 'ignore')
    else:
        print _str


class TestUnicode(unittest.TestCase):
    """test: Unicode."""

    def test_unicode(self):
        """test unicode handling.
        """
        print

        # Type conversion
        # unicode -> encode -> str
        # str     -> decode -> unicode

        utf_8_unicode = u'Wächter'
        print 'This type is unicode: ', type(utf_8_unicode)

        utf_8_unicode_str = utf_8_unicode.encode('utf-8', 'ignore')
        print 'This type is str:     ', type(utf_8_unicode_str)

        # print always convert to str. If the unicode is given, it
        # will be encoded. Therefore, the next failes with
        #
        # UnicodeEncodeError ascii' codec can't encode character
        # u'\xe4' in position 1: ordinal not in range(128)
        #
        try:
            print utf_8_unicode
        except UnicodeEncodeError as e:
            print 'UnicodeEncodeError raised: ' + str(e)

        # But this works, since it has already encoded to str type.
        print utf_8_unicode.encode('utf-8', 'ignore')

        # Here is a convenient function.
        # print_str('print_str: ' + utf_8_unicode)

        # However this doesn't work. unicode is encoded to string in
        # format(), but it becomes type str, then formet try to decode
        # to unicode. This failed.
        try:
            print u'unicode with format: {0}'.format(utf_8_unicode.encode('utf-8', 'ignore'))
        except UnicodeDecodeError as e:
            print 'UnicodeDecodeError raised: ' + str(e)

        # Because, u'string' is type unicode. print will convert to type str.
        # Therefore, the next works. Note, this is very small difference.
        print u'unicode with format works: {0}'.format(utf_8_unicode).encode('utf-8', 'ignore')

        # ustr = u'unicode with format works: {0}'.format(utf_8_unicode)
        # print_str(ustr)


        # 78 111 235 108 ... This is utf-8. Not the Unicode (code point).
        for c in utf_8_unicode:
            print ord(c),
        print

        # This is the unicode (code point), but type str.
        unicode_internal_str = utf_8_unicode.encode('unicode_internal')
        # 78 0 0 0 111 0 0 0 235 0 0 0 108 0 0 0 is the python internal string
        for c in unicode_internal_str:
            print ord(c),
        print
        print type(unicode_internal_str)



        # short form for explanation
        uc = u'Wächter'
        print type(uc)

        s = uc.encode('utf-8', 'ignore')
        print type(s)
        try:
            print uc
        except UnicodeEncodeError as e:
            print 'UnicodeEncodeError raised: ' + str(e)

        print uc.encode('utf-8', 'ignore')

        try:
            print u'{0}'.format(uc.encode('utf-8', 'ignore'))
        except UnicodeDecodeError as e:
            print 'UnicodeDecodeError raised: ' + str(e)

        print u'{0}'.format(uc).encode('utf-8', 'ignore')






    #def test_unicode_file(self):
    #    """test loading unicode (utf-8) encoded file.
    #    """
    #    infile = codecs.open('test_unicode_data.txt', mode='r', encoding='utf-8')


#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestUnicode)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)

