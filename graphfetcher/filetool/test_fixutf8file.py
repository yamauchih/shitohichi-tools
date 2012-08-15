#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Yamauchi, Hitoshi
# For Rebecca from Hitoshi the fool
#
# fix utf-8 file test
#
"""
\file
\brief fix utf-8 file test
"""

import FixUtf8File
import unittest

class TestUtf8File(unittest.TestCase):
    """test: FixUtf8File test."""

    def test_fix_utf8_file(self):
        """test fixing utf8 file corruption test."""
        graphfetcherdir   = u'/home/hitoshi/data/project/shitohichi-tools/graphfetcher/'
        input_rpath       = u'data/japanese_writer/ja.wikipedia.org/wiki/'
        output_rpath      = u'data/japanese_writer/ja.wikipedia.org/wiki_fixed/'
        input_fullpath    = graphfetcherdir + input_rpath
        output_fullpath   = graphfetcherdir + output_rpath
        print u'\n# input  dir [' + input_fullpath  + u']'
        print u'\n# output dir [' + output_fullpath + u']'


        # error handling {'strict', 'replace', 'ignore' }
        opt_dict = { 'encoding_errors':'ignore' }

        fixutf = FixUtf8File.FixUtf8File(opt_dict)
        fixutf.fix_all_file(input_fullpath, output_fullpath)

#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestUtf8File)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)


