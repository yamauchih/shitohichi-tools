#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Yamauchi, Hitoshi
# For Rebecca from Hitoshi the fool
#
# GraphExtractor test
#
"""
\file
\brief GraphExtractor test
"""

import GraphExtractor
import unittest

class TestGraphExtractor(unittest.TestCase):
    """test: GraphExtractor test."""

    def test_listfetcher(self):
        """test graph (adjacent matrix) extractor."""
        # print u'# Need LC_ALL setting to utf-8, e.g., en_US.utf-8, ja_JP.utf-8.'
        graphfetcherdir = u'/home/hitoshi/data/project/shitohichi-tools/graphfetcher/'
        wikidatadir     = u'data/ja.wikipedia.org/wiki/'
        input_list_fname   = u'nihonno_shousetuka_ichiran.list'
        output_M_adj_fname = u'nihonno_shousetuka_ichiran.Madj'
        input_path  = graphfetcherdir + wikidatadir + input_list_fname
        output_path = graphfetcherdir + wikidatadir + output_M_adj_fname
        print u'# input [' + input_path  + u']'
        print u'# output[' + output_path + u']'
        ge = GraphExtractor.GraphExtractor()
        ge.get_adjacebt_matrix(input_path, output_path)

#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestGraphExtractor)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)


