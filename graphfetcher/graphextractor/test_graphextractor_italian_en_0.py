#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012-2013 Yamauchi, Hitoshi
# For Rebecca from Hitoshi the fool
#
# GraphExtractor test
#
"""
\file
\brief GraphExtractor test: italian_en (Italian writer on English wiki)
"""

import GraphExtractor
import os, unittest, filecmp

class TestGraphExtractor(unittest.TestCase):
    """test: GraphExtractor test."""

    def test_graphextractor(self):
        """test graph (adjacent matrix) extractor. italian_en Italian Writer, English Wiki"""

        # basic configuration
        data_lang         = u'italian'
        wiki_lang         = u'en'
        author_root_fname = u'List_of_Italian_writers'

        #
        # directory set up
        #
        # print u'# Need LC_ALL setting to utf-8, e.g., en_US.utf-8, ja_JP.utf-8.'
        graphfetcherdir    = u'/home/hitoshi/data/project/shitohichi-tools/graphfetcher/'
        data_dir           = u'data/' + data_lang + u'_writer/'

        input_rpath        = data_dir + wiki_lang + u'.wikipedia.org/'
        output_rpath       = data_dir + wiki_lang + u'.wikipedia.org/'
        input_vector_fname = data_lang + '_' + wiki_lang + u'_writer.utf-8.vector'
        output_madj_fname  = data_lang + '_' + wiki_lang + u'_writer_adj_mat.m'

        input_html_dir     = graphfetcherdir + input_rpath  + 'wiki/'
        input_vector_fpath = graphfetcherdir + input_rpath  + input_vector_fname
        output_html_dir    = graphfetcherdir + output_rpath + 'wiki_out/'
        output_madj_fpath  = graphfetcherdir + output_rpath + output_madj_fname

        print
        print u'# input html dir    [' + input_html_dir     + u']'
        print u'# input vector file [' + input_vector_fpath + u']'
        print u'# output dir        [' + output_html_dir    + u']'
        print u'# output madj file  [' + output_madj_fpath  + u']'

        # options
        opt_dict = {
            # see ILog
            'log_level': 1,
            # When print out connection, set this True
            'is_print_connectivity': False,
            # When the entry is UTF8 and conversion failed, try set this.
            'is_enable_stdout_utf8_codec': False,
            # When output the dot (graphviz) file, set non empty file name (e.g., a.dot)
            'dot_file_name': data_lang + '_' + wiki_lang + '_writer_adj_mat.dot',
            # When True, generate annotated html file
            'is_generate_annotated_html': False,
            # When True, remove self link
            'is_remove_self_link': True,
            # Output matrix type ['python', 'matlab']
            'output_matrix_type': 'matlab',
            # do you want to remove the navbox entries?
            # Note: This is the main difference with test_graphextractor_italy_en_1.py
            'is_remove_navbox': False
            }

        tracelist = []
        ge = GraphExtractor.GraphExtractor(tracelist, opt_dict)

        ge.get_adjacent_matrix(input_html_dir,  input_vector_fpath,
                               output_html_dir, output_madj_fpath)

        # compare to the baseline file
        ref_fname = os.path.join(graphfetcherdir,
                                 'graphextractor/baseline/' + output_madj_fname)
        if(os.path.isfile(ref_fname)):
            self.assertEqual(filecmp.cmp(output_madj_fpath, ref_fname), True)
        else:
            print 'not found basefile [' + ref_fname + ']'

#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestGraphExtractor)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)
