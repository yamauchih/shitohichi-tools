#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012-2013 Yamauchi, Hitoshi
#
# LinkVectorExtractor test: italian_en (Italian Writer, English Wiki)
#
"""
\file
\brief LinkVectorExtractor test: italian_en (Italian Writer, English Wiki)
"""

import os
import LinkVectorExtractor
import unittest, filecmp

class TestLinkVectorExtractor(unittest.TestCase):
    """test: LinkVectorExtractor test."""

    def linkvectorextractor(self, _opt_dict):
        """test generate URL list by List of Italian writers from
        English wiki (italian_en).  The export encoding option 'ascii'
        gives you matlab readable author vector.
        """
        # basic configuration
        data_lang         = u'italian'
        wiki_lang         = u'en'
        author_root_fname = u'List_of_Italian_writers'

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
            '../w/index.php', 'Category', '/wiki', 'Wikipedia:', 'Portal',
            "List_of_children's_literature_authors",
            'List_of_English_novelists',
            'List_of_Italian_writers',
            'Lists_of_writers',
            'English_literature',
            'English_novel',
            'Main_Page',
            'Help:Contents',
            'Special:Random',
            'Special:RecentChanges',
            'Special:RecentChangesLinked/List_of_Italian_writers',
            'Special:SpecialPages',
            'Special:WhatLinksHere/List_of_Italian_writers',
            'Talk:List_of_Italian_writers',
            '/w/index.php?title=List_of_Italian_writers&oldid=494209347',
            '/w/index.php?title=Special:Book&bookcmd=book_creator&referer=List+of+English+writers',
            '/w/index.php?title=Special:Cite&page=List_of_Italian_writers&id=494209347'
            ]

        # what tag have the links?
        _opt_dict['tag_in_each_link'] = 'li'

        output_list_fname = output_list_basename + '.' + _opt_dict['export_encoding'] + '.vector'
        output_full_path = os.path.join(outdir, output_list_fname)
        print u'# output[' + output_full_path + u']'


        lf = LinkVectorExtractor.LinkVectorExtractor(ignore_href_list, _opt_dict)
        lf.get_link_list(root_url)
        lf.export_to_file(output_full_path)

        # return
        return (output_full_path, output_list_fname)


    def test_linkvectorextractor_ascii(self):
        opt_dict = {'export_encoding': 'ascii'}
        # opt_dict = {'export_encoding': 'shift-jis'}
        (output_full_path, output_fname) = self.linkvectorextractor(opt_dict)

        # compare to the baseline file
        ref_fname = os.path.join('baseline', output_fname)
        self.assertEqual(filecmp.cmp(output_full_path, ref_fname), True)


    def test_linkvectorextractor_utf8(self):
        opt_dict = {'export_encoding': 'utf-8'}
        (output_full_path, output_fname) = self.linkvectorextractor(opt_dict)

        # compare to the baseline file
        ref_fname = os.path.join('baseline', output_fname)
        self.assertEqual(filecmp.cmp(output_full_path, ref_fname), True)


#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestLinkVectorExtractor)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)

# Duplication list
#
