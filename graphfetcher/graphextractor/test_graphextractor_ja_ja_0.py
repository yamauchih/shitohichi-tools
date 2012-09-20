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
        graphfetcherdir   = u'/home/hitoshi/data/project/shitohichi-tools/graphfetcher/'
        input_rpath       = u'data/japanese_writer/ja.wikipedia.org/'
        output_rpath      = u'data/japanese_writer/ja.wikipedia.org/'
        input_vector_fname  = u'ja_ja_writer.list'
        output_madj_fname = u'ja_ja_writer_adj_mat_selected.m'

        input_html_dir     = graphfetcherdir + input_rpath  + 'wiki/'
        input_vector_fpath = graphfetcherdir + input_rpath  + 'ja_ja_writer.vector'
        output_html_dir    = graphfetcherdir + output_rpath + 'wiki_out/'
        output_madj_fpath  = graphfetcherdir + output_rpath + output_madj_fname

        print
        print u'# input html dir    [' + input_html_dir     + u']'
        print u'# input vector file [' + input_vector_fpath + u']'
        print u'# output dir        [' + output_html_dir    + u']'
        print u'# output madj file  [' + output_madj_fpath  + u']'

        # options
        opt_dict = {
            # When print out connection, set this True
            'is_print_connectivity': False,
            # When output the dot (graphviz) file, set non empty file name (e.g., a.dot)
            'dot_file_name': 'selected.dot',
            # When True, generate annotated html file
            'is_generate_annotated_html': False,
            # When True, remove self link
            'is_remove_self_link': True,
            # Output matrix type ['python', 'matlab']
            'output_matrix_type': 'matlab'
            }
        # ge = GraphExtractor.GraphExtractor([], opt_dict)
        # ge = GraphExtractor.GraphExtractor([u'三島由紀夫', u'大江健三郎'], opt_dict)
        # ge = GraphExtractor.GraphExtractor([u'八切止夫'], opt_dict)
        ge = GraphExtractor.GraphExtractor([u'三島由紀夫', u'大江健三郎', u'芥川龍之介',
                                            u'阿刀田高',   u'江戸川乱歩', u'遠藤周作',
                                            u'加納朋子',   u'村上春樹',   u'武者小路実篤',
                                            u'夏目漱石' ], opt_dict)

        ge.get_adjacent_matrix(input_html_dir,  input_vector_fpath,
                               output_html_dir, output_madj_fpath)

#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestGraphExtractor)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)

