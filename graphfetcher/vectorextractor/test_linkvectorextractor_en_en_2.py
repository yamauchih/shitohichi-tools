#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Yamauchi, Hitoshi
#
# LinkVectorExtractor test with a small dataset
#
"""
\file
\brief LinkVectorExtractor test
"""

import os
import LinkVectorExtractor
import unittest, filecmp

class TestLinkVectorExtractor(unittest.TestCase):
    """test: LinkVectorExtractor test."""

    def linkvectorextractor(self, _opt_dict):
        """test generate URL list by List of English writers (en_en)."""
        # print u'# Need LC_ALL setting to utf-8, e.g., en_US.utf-8, ja_JP.utf-8.'
        graphfetcherdir = u'/home/hitoshi/data/project/shitohichi-tools/graphfetcher/'

        # input_rpath       = u'data/english_writer/en.wikipedia.org/wiki/'
        # author_root_fname = u'List_of_English_writers'
        input_rpath       = u'vectorextractor/'
        author_root_fname = u'en_en_testdata_0.html'

        indir = os.path.join(graphfetcherdir, input_rpath)
        input_fullpath = os.path.join(indir, author_root_fname)
        root_url    = u'file:///' + input_fullpath

        output_rpath         = u'data/english_writer/en.wikipedia.org/wiki/'
        output_list_basename = u'en_en_2_writer'
        outdir = os.path.join(graphfetcherdir, output_rpath)

        print
        print u'# input [' + root_url    + u']'
        ignore_href_list = [
            '../w/index.php', 'Category', '/wiki', 'Wikipedia:', 'Portal'  ]

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


