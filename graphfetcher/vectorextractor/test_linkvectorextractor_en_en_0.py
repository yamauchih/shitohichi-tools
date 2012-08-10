#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Yamauchi, Hitoshi
#
# LinkVectorExtractor test
#
"""
\file
\brief LinkVectorExtractor test
"""

import os
import LinkVectorExtractorEnEn
import unittest

class TestLinkVectorExtractor(unittest.TestCase):
    """test: LinkVectorExtractor test."""

    def test_linkvectorextractor(self):
        """test generate URL list by List of English writers (en_en)."""
        # print u'# Need LC_ALL setting to utf-8, e.g., en_US.utf-8, ja_JP.utf-8.'
        graphfetcherdir = u'/home/hitoshi/data/project/shitohichi-tools/graphfetcher/'

        input_rpath       = u'data/english_writer/en.wikipedia.org/wiki/'
        author_root_fname = u'List_of_English_writers'

        indir = os.path.join(graphfetcherdir, input_rpath)
        input_fullpath = os.path.join(indir, author_root_fname)
        root_url    = u'file:///' + input_fullpath

        output_rpath      = u'data/english_writer/en.wikipedia.org/'
        output_list_fname = u'en_en_writer.vector'
        outdir = os.path.join(graphfetcherdir, output_rpath)
        output_full_path = os.path.join(outdir, output_list_fname)

        print u'# input [' + root_url    + u']'
        print u'# output[' + output_full_path + u']'
        ignore_href_list = [
            '../w/index.php', 'Category', '/wiki', 'Wikipedia:', 'Portal',
            "List_of_children's_literature_authors",
            'List_of_English_novelists',
            'List_of_English_writers',
            'Lists_of_writers',
            'English_literature',
            'English_novel',
            'Main_Page',
            'Help:Contents',
            'Special:Random',
            'Special:RecentChanges',
            'Special:RecentChangesLinked/List_of_English_writers',
            'Special:SpecialPages',
            'Special:WhatLinksHere/List_of_English_writers',
            'Talk:List_of_English_writers',
            '/w/index.php?title=List_of_English_writers&oldid=494209347',
            '/w/index.php?title=Special:Book&bookcmd=book_creator&referer=List+of+English+writers',
            '/w/index.php?title=Special:Cite&page=List_of_English_writers&id=494209347'
            ]

        # optdict = {'export_encoding': 'utf-8'}
        optdict = {'export_encoding': 'ascii'}
        # optdict = {'export_encoding': 'shift-jis'}
        lf = LinkVectorExtractorEnEn.LinkVectorExtractorEnEn(ignore_href_list, optdict)
        lf.get_link_list(root_url, output_full_path)


#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestLinkVectorExtractor)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)


