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

    def test_graphextractor(self):
        """test graph (adjacent matrix) extractor."""
        # print u'# Need LC_ALL setting to utf-8, e.g., en_US.utf-8, ja_JP.utf-8.'
        graphfetcherdir = u'/home/hitoshi/data/project/shitohichi-tools/graphfetcher/'
        wikidatadir     = u'data/japanese_writer/ja.wikipedia.org/wiki/'
        input_list_fname   = u'nihonno_shousetuka_ichiran.list'
        # output_M_adj_fname = u'nihonno_shousetuka_ichiran.Madj'
        output_M_adj_fname = u'00test.Madj'
        working_path  = graphfetcherdir + wikidatadir
        print u'\n# input [' + working_path  + u'], filename[' + input_list_fname + u']'
        print u'# filename[' + output_M_adj_fname + u']'

        # ge = GraphExtractor.GraphExtractor(None)
        ge = GraphExtractor.GraphExtractor([u'三島由紀夫', u'大江健三郎'])
        ge.get_adjacebt_matrix(working_path, input_list_fname, output_M_adj_fname)

#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestGraphExtractor)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)


