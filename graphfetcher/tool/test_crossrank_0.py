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

import unittest, re, os, filecmp
import CrossRank

class TestCrossRank(unittest.TestCase):
    """test: cross rank."""

    def test_umlaut_replace(self):
        """How to replace the unicode charactor"""
        s = u'AE = Ä'
        rep = re.sub(u'Ä', u'\\"{AE}', s, 0, re.UNICODE)
        self.assertEqual(rep, u'AE = \\"{AE}')


    def _test_umlaut_replace_a(self):
        """How to replace the unicode charactor"""
        # 0.079 sec if no umlaut
        # 2.143 sec if there is a umlaut charactor

        # s = u'AE = Ä, ae = ä, OE = Ö, oe = ö, UE = Ü, ue = ü, ss = ß'

        s = u'Friedrich_Hölderlin'
        uml_A = re.compile(u'Ä', re.UNICODE)
        uml_a = re.compile(u'ä', re.UNICODE)
        uml_O = re.compile(u'Ö', re.UNICODE)
        uml_o = re.compile(u'ö', re.UNICODE)
        uml_U = re.compile(u'Ü', re.UNICODE)
        uml_u = re.compile(u'ü', re.UNICODE)
        szet  = re.compile(u'ß', re.UNICODE)
        uml_all = re.compile(u'[ÄäÖöÜüß]', re.UNICODE)

        for i in range(1, 100000):
            # s = u'Friedrich_Hölderlin'
            s = u'Friedrich_Hoelderlin'
            if(uml_all.search(s) != None):
                uml_A.sub(u'\\"{AE}', s)
                uml_a.sub(u'\\"{ae}', s)
                uml_O.sub(u'\\"{OE}', s)
                uml_o.sub(u'\\"{oe}', s)
                uml_U.sub(u'\\"{UE}', s)
                uml_u.sub(u'\\"{ue}', s)
                szet .sub(u'{\\ss}',  s)

    def _test_umlaut_replace_b(self):
        """How to replace the unicode charactor"""
        # 1.998 sec if no umlaut
        # 2.078 sec if there is a umlaut charactor

        uml_A = re.compile(u'Ä', re.UNICODE)
        uml_a = re.compile(u'ä', re.UNICODE)
        uml_O = re.compile(u'Ö', re.UNICODE)
        uml_o = re.compile(u'ö', re.UNICODE)
        uml_U = re.compile(u'Ü', re.UNICODE)
        uml_u = re.compile(u'ü', re.UNICODE)
        szet  = re.compile(u'ß', re.UNICODE)
        uml_all = re.compile(u'[ÄäÖöÜüß]', re.UNICODE)

        for i in range(1, 100000):
            # s = u'Friedrich_Hölderlin'
            s = u'Friedrich_Hoelderlin'
            uml_A.sub(u'\\"{AE}', s)
            uml_a.sub(u'\\"{ae}', s)
            uml_O.sub(u'\\"{OE}', s)
            uml_o.sub(u'\\"{oe}', s)
            uml_U.sub(u'\\"{UE}', s)
            uml_u.sub(u'\\"{ue}', s)
            szet .sub(u'{\\ss}',  s)


    def test_cross_rank_inout(self):
        """test cross rank input/output."""

        out_fname = 'test_crossrank_res.txt'

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
