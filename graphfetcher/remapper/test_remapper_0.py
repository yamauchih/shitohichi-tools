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
\brief Remapper test
"""

import Remapper
import os, unittest, filecmp

class TestRemapper(unittest.TestCase):
    """test: Remapper test."""

    def remapper_sub(self,  _data_prefix):
        """test remapper subroutine.
        \param[in] _data_prefix data prefix. e.g., en_de, ja_ja, ...
        """

        # Rebecca, this is the root directory.
        graphfetcherdir    = u'/home/hitoshi/data/project/shitohichi-tools/graphfetcher/'

        # rpath is relative path from the graphfetcher (= root)
        in_vector_rpath    = u'vectorextractor/baseline/'
        in_rankdata_rpath  = u'pagerank/pagerank_result/'
        out_save_rpath     = graphfetcherdir + u'remapper/'

        # fname is only the file name
        in_vector_fname    = _data_prefix + u'_writer.utf-8.vector'
        in_rankdata_fname  = _data_prefix + u'_writer.pagerank.data'
        out_save_fname     = _data_prefix + u'_writer_ranked.vector'

        # fpath is full path of the file.
        in_vector_fpath    = graphfetcherdir + in_vector_rpath   + in_vector_fname
        in_rankdata_fpath  = graphfetcherdir + in_rankdata_rpath + in_rankdata_fname
        out_save_fpath     = out_save_rpath + out_save_fname

        # options
        opt_dict = {
            # log level: int. 0 ... error, 1 ... info, 2 ... debug
            'log_level': 0,
            # enable stdout utf8 codec
            'is_enable_stdout_utf8_codec': False,
            }

        rmap = Remapper.Remapper(opt_dict)
        rmap.remap_author(in_vector_fpath, in_rankdata_fpath, out_save_fpath)

        # compare to the baseline file
        ref_fpath = os.path.join(graphfetcherdir,
                                 'remapper/baseline/' + out_save_fname)
        if(os.path.isfile(ref_fpath)):
            self.assertEqual(filecmp.cmp(out_save_fpath, ref_fpath), True)
        else:
            print 'not found basefile [' + ref_fpath + ']'
            # When generate the baseline, comment the following line out.
            self.assertTrue(False)


    def test_remapper(self):
        """test remapper all language, all wiki."""

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
            print 'testing [' + i + ']... passed.'

#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestRemapper)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)
