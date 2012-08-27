#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Yamauchi, Hitoshi
#
# LinkVectorExtractor test: ja_en (Japanese Writer, English Wiki)
#
"""
\file
\brief LinkVectorExtractor test: ja_en (Japanese Writer, English Wiki)
"""

import os
import LinkVectorExtractor
import unittest

class TestLinkVectorExtractor(unittest.TestCase):
    """test: LinkVectorExtractor test."""

    def test_linkvectorextractor(self):
        """test generate URL list by List of Japanese writers from English wiki (ja_en).
        The export encoding option 'ascii' gives you matlab readable author vector.
        """
        # print u'# Need LC_ALL setting to utf-8, e.g., en_US.utf-8, ja_JP.utf-8.'
        graphfetcherdir = u'/home/hitoshi/data/project/shitohichi-tools/graphfetcher/'

        input_rpath       = u'data/japanese_writer/en.wikipedia.org/wiki/'

        # if substring of the following list matches the href, ignore.
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
            'List_of_Japanese_writers',
            '/w/index.php?title=',
            'http://en.wikipedia.org/w/index.php?title=Special:UserLogin'
            ]

        author_root_fname = u'List_of_Japanese_writers:_'
        # List_of_Japanese_writers:_[A-Z], but some of them are not there, (e.g., X)
        author_first_char_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                                  'M', 'N', 'O', 'R', 'S', 'T', 'U', 'W', 'Y', 'Z' ]

        output_rpath      = u'data/japanese_writer/en.wikipedia.org/'
        outdir = os.path.join(graphfetcherdir, output_rpath)

        output_list_fname = u'ja_en_writer.vector'
        # output_list_fname = u'en_en_writer.ascii.vector'
        output_full_path = os.path.join(outdir, output_list_fname)

        # optdict = {'export_encoding': 'utf-8'}
        optdict = {'export_encoding': 'ascii'}
        # optdict = {'export_encoding': 'shift-jis'}

        lf = LinkVectorExtractor.LinkVectorExtractor(ignore_href_list, optdict)

        for prefix_ch in author_first_char_list:
            indir = os.path.join(graphfetcherdir, input_rpath)
            input_fullpath = os.path.join(indir, author_root_fname + prefix_ch)
            root_url    = u'file:///' + input_fullpath

            print u'# input [' + root_url    + u']'
            lf.get_link_list(root_url)

        print u'# export [' + output_full_path + u']'
        lf.export_to_file(output_full_path)


#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestLinkVectorExtractor)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)

# Duplication list
#
# info: found duplication [Noël_Coward]
# info: found duplication [Pierce_Egan]
# info: found duplication [Douglas_William_Jerrold]
# info: found duplication [Jane_Marcet]
# info: found duplication [Henry_Peacham]
# info: found duplication [Adelaide_Anne_Procter]
# info: found duplication [Mary_Sidney]
# info: found duplication [Lisa_St_Aubin_de_Terán]
# info: found duplication [Anne_Isabella_Thackeray_Ritchie]
# info: found duplication [William_Wycherley]
