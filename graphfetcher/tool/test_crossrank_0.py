#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Yamauchi, Hitoshi
# For Rebecca from Hitoshi the fool
#
# test CrossRank
#
"""
\file
\brief cross ranking test
"""

import unittest, re
import CrossRank

class TestCrossRank(unittest.TestCase):
    """test: cross rank."""

    def test_umlaut_replace(self):
        """How to replace the unicode charactor"""

        # s = u'AE = Ä, ae = ä, OE = Ö, oe = ö, UE = Ü, ue = ü, ss = ß'
        s = u'AE = Ä'
        rep = re.sub(u'Ä', u'\\"{AE}', s, 0, re.UNICODE)
        self.assertEqual(rep, u'AE = \\"{AE}')


    def test_cross_rank_inout(self):
        """test cross rank input output."""

        opt_dict = {
            'base_fname': 'baseline/test_de_de_writer_ranked.vector',
            'ref_fname':  'baseline/test_de_en_writer_ranked.vector',
            'out_fname':  'test_crossref.txt',
            'is_tex_table':                True,
            'is_tex_umlaut':               False,
            'is_add_line_number':          True,
            'is_rank_out':                 True,
            'is_enable_stdout_utf8_codec': True
            }

        cr = CrossRank.CrossRank(opt_dict)
        cr.show_cross_rank()


#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestCrossRank)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)
