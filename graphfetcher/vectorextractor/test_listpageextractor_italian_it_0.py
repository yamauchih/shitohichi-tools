#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012-2013 Yamauchi, Hitoshi
#
# ListPageExtractorItalian: italian_it (Italian Writer, Italian Wiki)
#
#   Italian wiki has not direct list link page. This script analyzes a
#   meta page and extracted direct link meta pages.
#
#
"""
\file
\brief ListPageExtractorItalian test: italian_it (Italian Writer, Italian Wiki)
"""

import os
import ListPageExtractorItalian
import unittest, filecmp

class TestListPageExtractor(unittest.TestCase):
    """test: LinkVectorExtractor test."""

    def listextractor(self, _opt_dict):
        """list page extractor test.
        """
        # basic configuration
        data_lang         = u'italian'
        wiki_lang         = u'it'
        author_root_fname = u'Categoria:Scrittori_italiani'

        #
        # directory set up
        #
        # print u'# Need LC_ALL setting to utf-8, e.g., en_US.utf-8, ja_JP.utf-8.'
        graphfetcherdir   = u'/home/hitoshi/data/project/shitohichi-tools/graphfetcher/'

        data_dir          = u'data/' + data_lang + u'_writer/'
        input_rpath       = data_dir + wiki_lang + u'.wikipedia.org/wiki/'

        indir = os.path.join(graphfetcherdir, input_rpath)
        input_fullpath = os.path.join(indir, author_root_fname)
        root_url    = u'file:///' + input_fullpath

        output_rpath         = data_dir + wiki_lang + u'.wikipedia.org/'
        output_list_basename = data_lang + '_' + wiki_lang + u'_writer'
        outdir = os.path.join(graphfetcherdir, output_rpath)

        print
        print u'# input [' + root_url    + u']'
        # if substring of the following list matches the href, ignore.
        # If exact match filter is needed, use blacklistset option.
        ignore_href_list = [
            ]

        # what tag have the links?
        _opt_dict['tag_in_each_link'] = 'li'

        output_list_fname = output_list_basename + '.' + _opt_dict['export_encoding'] + '.vector'
        output_full_path = os.path.join(outdir, output_list_fname)
        print u'# output[' + output_full_path + u']'


        lf = ListPageExtractorItalian.ListPageExtractorItalian(ignore_href_list, _opt_dict)
        lf.get_link_list(root_url)

        # return
        # return (output_full_path, output_list_fname)


    def test_listextractor(self):
        opt_dict = {'export_encoding': 'ascii'}
        # opt_dict = {'export_encoding': 'shift-jis'}
        self.listextractor(opt_dict)

        # compare to the baseline file
        # ref_fname = os.path.join('baseline', output_fname)
        # self.assertEqual(filecmp.cmp(output_full_path, ref_fname), True)


#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestListPageExtractor)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)

