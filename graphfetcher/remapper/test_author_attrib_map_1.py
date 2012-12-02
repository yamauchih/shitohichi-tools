#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Yamauchi, Hitoshi
# For Rebecca from Hitoshi the fool
#
# author attribute mapper test with Akutagawa award winner
#
"""
\file
\brief Author attribute mapper
"""

import AuthorAttributeMapper
import os, unittest, filecmp

class TestAuthorAttributeRemapper(unittest.TestCase):
    """test: author attribute mapper test."""

    def test_author_attribute_mapper(self):
        """test author attribute mapper."""

        opt_dict = {
            # akutagawa_winner.vector's attribute 0 (n-th_winner)
            'output_attrib_idx': 0
            }

        rootdir    = '/home/hitoshi/data/project/shitohichi-tools/graphfetcher/'

        author_vec_fname    = 'ja_ja_writer_author.vector'
        author_attrib_fname = 'akutagawa_winner.vector'
        save_fname          = 'ja_ja_akutagawa_winner_attrib.vector'
        author_vec_fpath    = os.path.join(rootdir, 'remapper/baseline', author_vec_fname)
        author_attrib_fpath = os.path.join(rootdir, 'remapper', author_attrib_fname)
        save_fpath          = os.path.join(rootdir, 'remapper', save_fname)

        aam = AuthorAttributeMapper.AuthorAttributeMapper(opt_dict)
        aam.map_attribute(author_vec_fpath, author_attrib_fpath, save_fpath)

        # compare to the baseline file
        ref_fpath = os.path.join(rootdir, 'remapper/baseline', save_fname)
        if(os.path.isfile(ref_fpath)):
            # print save_fpath, ref_fpath
            self.assertEqual(filecmp.cmp(save_fpath, ref_fpath), True)
        else:
            print 'not found basefile [' + ref_fpath + ']'
            # When generate the baseline, comment the following line out.
            self.assertTrue(False)



#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestAuthorAttributeRemapper)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)
