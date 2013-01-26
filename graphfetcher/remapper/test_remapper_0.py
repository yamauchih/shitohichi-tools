#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012-2013 Yamauchi, Hitoshi
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

    def remapper_sub(self,  _data_prefix, _opt_dict):
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
        if ('vecname_prefix' in  _opt_dict):
            in_vector_fname = _opt_dict['vecname_prefix'] + u'_writer.utf-8.vector'
        else:
            in_vector_fname = _data_prefix + u'_writer.utf-8.vector'
        in_rankdata_fname  = _data_prefix + u'_writer.pagerank.data'
        out_save_fname     = _data_prefix + u'_writer_author_rank.vector'

        # fpath is full path of the file.
        in_vector_fpath    = graphfetcherdir + in_vector_rpath   + in_vector_fname
        in_rankdata_fpath  = graphfetcherdir + in_rankdata_rpath + in_rankdata_fname
        out_save_fpath     = out_save_rpath + out_save_fname

        # options
        opt_dict = {
            # log level: int. 0 ... error, 1 ... info, 2 ... debug
            'log_level': 3,
            # enable stdout utf8 codec
            'is_enable_stdout_utf8_codec': False,
            }

        rmap = Remapper.Remapper(opt_dict)
        rmap.remap_author(in_vector_fpath, in_rankdata_fpath, out_save_fpath)

        # compare to the baseline file
        ref_fpath = os.path.join(graphfetcherdir,
                                 'remapper/baseline/' + out_save_fname)
        if(os.path.isfile(ref_fpath)):
            print out_save_fpath, ref_fpath

            self.assertEqual(filecmp.cmp(out_save_fpath, ref_fpath), True)
        else:
            print 'not found basefile [' + ref_fpath + ']'
            # When generate the baseline, comment the following line out.
            self.assertTrue(False)


    def test_remapper_all(self):
        """test remapper all language, all wiki."""

        data_prefix_list = [
            {'de_de': {}},
            {'de_en': {}},
            {'de_ja': {}},
            {'en_de': {}},
            {'en_en': {}},
            {'en_ja': {}},
            {'ja_de': {}},
            {'ja_en': {}},
            {'ja_ja': {}},
            {'ja_ja_with_navbox': {}},
            {'italian_en': {}},
            {'italian_en_no_navbox': { 'vecname_prefix': 'italian_en'}}
            ]

        for i in data_prefix_list:
            key = i.keys()[0]
            print 'testing [' + key + ']... passed.'
            self.remapper_sub(key, i[key])

    def test_remapper_one(self):
        """test one remapper."""
        pass
        # self.remapper_sub(u'italian_en_no_navbox', { 'vecname_prefix': 'italian_en'})


#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestRemapper)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)
