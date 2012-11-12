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

    def test_cross_rank_inout(self):
        """test cross rank input/output."""

        out_fname = 'test_crossrank_res.txt'

        base_prefix

        base_fname = '../remapper/baseline/de_de_writer_ranked.vector'
        ref0_fname = '../remapper/baseline/de_en_writer_ranked.vector'
        ref1_fname = '../remapper/baseline/de_ja_writer_ranked.vector'


        opt_dict = {
            'base_fname': 'baseline/test_de_de_writer_ranked.vector',
            'ref_fname':  'baseline/test_de_en_writer_ranked.vector',
            'out_fname':  out_fname,
            'is_tex_table':                True,
            'is_tex_umlaut':               True,
            'is_add_line_number':          True,
            'is_rank_out':                 True,
            'is_enable_stdout_utf8_codec': True
            }

        cr = CrossRank.CrossRank(opt_dict)
        cr.show_cross_rank()

        # compare to the baseline file
        ref_fname = os.path.join('baseline/' + out_fname)
        if(os.path.isfile(ref_fname)):
            self.assertEqual(filecmp.cmp(out_fname, ref_fname), True)
        else:
            print 'not found basefile [' + ref_fname + ']'




#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestCrossRank)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)
