#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Yamauchi, Hitoshi
# For Rebecca from Hitoshi the fool
#
# Remapper test
#
"""
\file
\brief Remapper: de_ja (Deutsche writer on Japanese wiki)
"""

import Remapper
import os, unittest, filecmp

class TestRemapper(unittest.TestCase):
    """test: Remapper test."""

    def remapper_sub(self,  _data_prefix):
        """test remapper subroutine.
        \param[in] _data_prefix data prefix. e.g., en_de
        """

        # data_prefix        = u'de_ja'
        graphfetcherdir    = u'/home/hitoshi/data/project/shitohichi-tools/graphfetcher/'
        in_vector_rpath    = u'vectorextractor/baseline/'
        in_rankdata_rpath  = u'pagerank/pagerank_result/'
        in_vector_fname    = _data_prefix + u'_writer.utf-8.vector'
        in_rankdata_fname  = _data_prefix + u'_writer.pagerank.data'

        in_vector_fpath    = graphfetcherdir + in_vector_rpath   + in_vector_fname
        in_rankdata_fpath  = graphfetcherdir + in_rankdata_rpath + in_rankdata_fname

        print
        print u'# input vector file   [' + in_vector_fpath   + u']'
        print u'# input rankdata file [' + in_rankdata_fpath + u']'

        # options
        opt_dict = {
            # log level: int. 0 ... error, 1 ... info, 2 ... debug
            'log_level': 1,
            # enable stdout utf8 codec
            'is_enable_stdout_utf8_codec': True,
            }

        rmap = Remapper.Remapper(opt_dict)
        rmap.remap_author(in_vector_fpath, in_rankdata_fpath)

        # compare to the baseline file
        # ref_fname = os.path.join(graphfetcherdir,
        #                          'graphextractor/baseline/' + output_madj_fname)
        # if(os.path.isfile(ref_fname)):
        #     self.assertEqual(filecmp.cmp(output_madj_fpath, ref_fname), True)
        # else:
        #     print 'not found basefile [' + ref_fname + ']'


    def test_remapper(self):
        """test remapper."""

        data_prefix_list = [
            u'de_de',
            u'de_en',
            u'de_ja',
            u'en_de',
            u'en_en',
            u'en_ja',
            u'ja_de',
            u'ja_en',
            u'ja_ja'
            ]

        for i in data_prefix_list:
            self.remapper_sub(i)

#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestRemapper)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)
