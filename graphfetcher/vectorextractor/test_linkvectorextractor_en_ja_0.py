#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Yamauchi, Hitoshi
#
# LinkVectorExtractor test: en_ja (English Writer, Japanese Wiki)
#
"""
\file
\brief LinkVectorExtractor test: en_ja (English Writer, Japanese Wiki)
"""

import os
import LinkVectorExtractor
import unittest, filecmp

class TestLinkVectorExtractor(unittest.TestCase):
    """test: LinkVectorExtractor test."""

    def linkvectorextractor(self, _opt_dict):
        """test generate URL list by List of English writers from
        Japanese wiki (en_ja).  The export encoding option 'ascii'
        gives you matlab readable author vector.
        """
        # print u'# Need LC_ALL setting to utf-8, e.g., en_US.utf-8, ja_JP.utf-8.'
        graphfetcherdir = u'/home/hitoshi/data/project/shitohichi-tools/graphfetcher/'

        input_rpath       = u'data/english_writer/ja.wikipedia.org/wiki/'
        author_root_fname = u'イギリスの小説家一覧'

        indir = os.path.join(graphfetcherdir, input_rpath)
        input_fullpath = os.path.join(indir, author_root_fname)
        root_url    = u'file:///' + input_fullpath

        output_rpath         = u'data/english_writer/ja.wikipedia.org/'
        output_list_basename = u'en_ja_writer'
        outdir = os.path.join(graphfetcherdir, output_rpath)

        print
        print u'# input [' + root_url    + u']'
        # if substring of the following list matches the href, ignore.
        # If exact match filter is needed, use blacklistset option.
        ignore_href_list = [
            '../w/index.php', 'Category', '/wiki', 'Wikipedia:', 'Portal',
            u'イギリスの小説家一覧',
            u'メインページ',
            u'特別:',
            'Help:'
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


    # def test_linkvectorextractor_ascii(self):
    #     opt_dict = {'export_encoding': 'ascii'}
    #     # opt_dict = {'export_encoding': 'shift-jis'}
    #     (output_full_path, output_fname) = self.linkvectorextractor(opt_dict)

    #     # compare to the baseline file
    #     ref_fname = os.path.join('baseline', output_fname)
    #     self.assertEqual(filecmp.cmp(output_full_path, ref_fname), True)


    def test_linkvectorextractor_utf8(self):
        opt_dict = {'export_encoding': 'utf-8'}
        (output_full_path, output_fname) = self.linkvectorextractor(opt_dict)

        # compare to the baseline file
        ref_fname = os.path.join('baseline', output_fname)
        self.assertEqual(filecmp.cmp(output_full_path, ref_fname), True)

        # make Latin charactor name list for matlab/octave
        self.assertEqual(filecmp.cmp(output_full_path, ref_fname), True)
        print 'convert to ascii'
        os.system('iconv -f UTF-8 -t EUC-JP baseline/en_ja_writer.utf-8.vector | kakasi -i euc -Ja -Ha -Ka -Ea > baseline/en_ja_writer.ascii.vector')


#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestLinkVectorExtractor)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)

# Duplication list
#
# info: found duplication [トーマス・ハーディ]
