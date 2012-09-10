#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Yamauchi, Hitoshi
#
# LinkVectorExtractor test: ja_ja (Japanese Writer, Japanese Wiki)
#
"""
\file
\brief LinkVectorExtractor test: ja_ja (Japanese Writer, Japanese Wiki)
"""

import os
import LinkVectorExtractor
import unittest

class TestLinkVectorExtractor(unittest.TestCase):
    """test: LinkVectorExtractor test."""

    def test_linkvectorextractor(self):
        """test 日本の小説家一覧を起点にした URL list を生成する．"""
        # print u'# Need LC_ALL setting to utf-8, e.g., en_US.utf-8, ja_JP.utf-8.'
        graphfetcherdir = u'/home/hitoshi/data/project/shitohichi-tools/graphfetcher/'

        input_rpath       = u'data/japanese_writer/ja.wikipedia.org/wiki/'
        author_root_fname = u'日本の小説家一覧'
        indir = os.path.join(graphfetcherdir, input_rpath)
        input_fullpath = os.path.join(indir, author_root_fname)
        root_url    = u'file:///' + input_fullpath

        output_rpath = u'data/japanese_writer/ja.wikipedia.org/'
        output_list_basename = u'ja_ja_writer.vector'
        outdir = os.path.join(graphfetcherdir, output_rpath)

        print u'# input [' + root_url    + u']'
        ignore_href_list = [
            '../w/index.php', 'Category', '/wiki', 'Wikipedia:', 'Portal', u'特別',
            'Help', 'http://wikimediafoundation.org', u'小説', u'作家', u'一覧',
            u'日本', u'メインページ', u'協定世界時' ]


        optdict = {'export_encoding': 'utf-8'}
        # optdict = {'export_encoding': 'ascii'}
        # optdict = {'export_encoding': 'shift-jis'}

        # what tag have the links?
        optdict['tag_in_each_link'] = 'li'

        output_list_fname = output_list_basename + '.' + optdict['export_encoding'] + '.vector'
        output_full_path = os.path.join(outdir, output_list_fname)
        lf = LinkVectorExtractor.LinkVectorExtractor(ignore_href_list, optdict)
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


