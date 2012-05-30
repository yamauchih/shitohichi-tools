#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Yamauchi, Hitoshi
#
# ListFetcher test
#
"""
\file
\brief ListFetcher test
"""

import ListFetcher
import unittest

class TestListFetcher(unittest.TestCase):
    """test: ListFetcher test."""

    def test_listfetcher(self):
        """test 日本の小説家一覧を起点にした URL list を生成する．"""
        # print u'# Need LC_ALL setting to utf-8, e.g., en_US.utf-8, ja_JP.utf-8.'
        graphfetcherdir = u'/home/hitoshi/data/project/shitohichi-tools/graphfetcher/'
        wikidatadir     = u'data/japanese_writer/ja.wikipedia.org/wiki/'
        author_root_fname = u'日本の小説家一覧'
        output_list_fname = u'nihonno_shousetuka_ichiran.list'
        root_url    = u'file:///' + graphfetcherdir + wikidatadir + author_root_fname
        output_path = graphfetcherdir + wikidatadir + output_list_fname
        # print u'# input [' + root_url    + u']'
        # print u'# output[' + output_path + u']'
        lf = ListFetcher.ListFetcher()
        lf.get_link_list(root_url, output_path)


#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestListFetcher)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)


