#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Yamauchi, Hitoshi
#
# FileVectorExtractor test for English wiki of English writers
#
"""
\file
\brief FileVectorExtractor test for English wiki of English writers
"""

import os
import FileVectorExtractor
import unittest

class TestFileVectorExtractorEnEn(unittest.TestCase):
    """test: FileVectorExtractorEnEn test."""

    def test_en_en(self):
        """test English weiter vector of """
        # print u'# Need LC_ALL setting to utf-8, e.g., en_US.utf-8, ja_JP.utf-8.'
        graphfetcherdir = u'/home/hitoshi/data/project/shitohichi-tools/graphfetcher/'

        input_rpath = u'data/english_writer/en.wikipedia.org/wiki/'
        input_dir   = os.path.join(graphfetcherdir, input_rpath)

        output_rpath      = u'data/english_writer/en.wikipedia.org/'
        output_list_fname = u'author_vector_en_en.vector'
        outdir = os.path.join(graphfetcherdir, output_rpath)
        output_full_path = os.path.join(outdir, output_list_fname)

        blist_rpath_fname = u'vectorextractor/en_en.blacklist'
        blist_full_path   = os.path.join(graphfetcherdir, blist_rpath_fname)

        print u'# input dir[' + input_dir + u']'
        print u'# output   [' + output_full_path + u']'
        print u'# blacklist[' + blist_full_path + u']'
        fve = FileVectorExtractor.FileVectorExtractor()
        fve.read_blacklist(blacklist_fname)
        fve.get_vector(input_dir, output_full_path)


#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestFileVectorExtractorEnEn)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)


