#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Yamauchi, Hitoshi
# For Rebecca from Hitoshi the fool
#
# urlencode the file: 石原慎太郎の file のみ圧縮がかかっており，この
# path が %xx escape されてしまっているので，これを修正する．
#
"""
\file
\brief fix utf-8 file test
"""

import urllib
import unittest

class TestURLEndcodeFile(unittest.TestCase):
    """test: FixUtf8File test."""

    def test_URL_encode_file(self):
        """test URL encode whole file."""

        fin = open('ishihara_shintaro', 'r')
        instr = fin.read()
        fin.close()

        unquote_str = urllib.unquote(instr)

        fout = open('ishihara_shintaro.unquote', 'w')
        fout.write(unquote_str);
        fout.close()

#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestURLEndcodeFile)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)
