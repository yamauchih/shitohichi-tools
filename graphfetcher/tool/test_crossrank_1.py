#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Yamauchi, Hitoshi
# For Rebecca from Hitoshi the fool
#
# get CrossRank result
#
"""
\file
\brief cross ranking result
"""

import unittest, re, os, filecmp
import CrossRank

class TestCrossRank(unittest.TestCase):
    """cross rank."""

    def cross_rank_sub(self, _base_code, _ref_code):
        """test cross rank input/output."""

        data_dir   = '../remapper/baseline'
        out_fpath  = _base_code + '_ref_' + _ref_code + '.txt'
        base_fname = _base_code + '_writer_author.vector'
        ref_fname  = _ref_code  + '_writer_author.vector'
        base_fpath = os.path.join(data_dir, base_fname)
        ref_fpath  = os.path.join(data_dir, ref_fname)

        opt_dict = {
            'base_fpath': base_fpath,
            'ref_fpath':  ref_fpath,
            'out_fpath':  out_fpath,
            'log_level':  4,
            'is_tex_table':                True,
            'is_tex_umlaut':               True,
            'is_add_line_number':          True,
            'is_rank_out':                 True,
            'is_enable_stdout_utf8_codec': True
            }

        cr = CrossRank.CrossRank(opt_dict)
        cr.show_cross_rank()

        # compare to the baseline file
        ref_fpath = os.path.join('baseline/' + out_fpath)
        if(os.path.isfile(ref_fpath)):
            self.assertEqual(filecmp.cmp(out_fpath, ref_fpath), True)
        else:
            print 'not found basefile [' + ref_fpath + ']'


    def test_cross_rank(self):
        """cross ranking test"""

        # ja can not use without Japanese Katakana -> Latin name map
        code_list = [
            # de pages cross reference
            ['de_de', 'de_en'],
            ['de_en', 'de_de'],
            # en pages cross reference
            ['en_en', 'en_de'],
            ['en_de', 'en_en']
            ]

        for code in code_list:
            self.cross_rank_sub(code[0], code[1])

#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestCrossRank)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)
