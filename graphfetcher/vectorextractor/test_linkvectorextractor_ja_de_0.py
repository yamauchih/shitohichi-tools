#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012-2013 Yamauchi, Hitoshi
#
# LinkVectorExtractor test: ja_de (Japanese Writer, Deutsche Wiki)
#
"""
\file
\brief LinkVectorExtractor test: ja_de (Japanese Writer, Deutsche Wiki)
"""

import os
import LinkVectorExtractor
import unittest, filecmp

class TestLinkVectorExtractor(unittest.TestCase):
    """test: LinkVectorExtractor test."""

    def linkvectorextractor(self, _opt_dict):
        """test generate URL list by List of Japanese writers from
        Deutsche wiki (ja_de).  The export encoding option 'ascii'
        gives you matlab readable author vector.
        """
        # print u'# Need LC_ALL setting to utf-8, e.g., en_US.utf-8, ja_JP.utf-8.'
        graphfetcherdir = u'/home/hitoshi/data/project/shitohichi-tools/graphfetcher/'

        input_rpath       = u'data/japanese_writer/de.wikipedia.org/wiki/'
        author_root_fname = u'Liste_japanischer_Schriftsteller'

        indir = os.path.join(graphfetcherdir, input_rpath)
        input_fullpath = os.path.join(indir, author_root_fname)
        root_url    = u'file:///' + input_fullpath

        output_rpath         = u'data/japanese_writer/de.wikipedia.org/'
        output_list_basename = u'ja_de_writer'
        outdir = os.path.join(graphfetcherdir, output_rpath)

        print
        print u'# input [' + root_url    + u']'
        # if substring of the following list matches the href, ignore.
        # If exact match filter is needed, use blacklistset option.
        ignore_href_list = [
            '../w/index.php', 'Category', '/wiki', 'Wikipedia:', 'Portal',
            'Heian-Zeit',
            'Japanisches_Mittelalter',
            'Edo-Zeit',
            u'Die_Sechsunddreißig_',
            'Liste_der_Dichter',
            'Liste_der_Mangaka',
            'Japanische_Literatur',
            'Schriftsteller',
            'Liste_von_Dichtern',
            'Liste_der_Biographien',
            'Kategorie:',
            'Liste_japanischer_Schriftsteller',
            'Diskussion:',
            'Spezial:',
            'Hilfe:',
            'Spezial:'
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


    def test_linkvectorextractor_ascii(self):
        opt_dict = {'export_encoding': 'ascii'}
        # opt_dict = {'export_encoding': 'shift-jis'}
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

# Duplication list
#
# info: found duplication [Isozaki_Kenichirō]
# info: found duplication [Shimaki_Kensaku]
# info: found duplication [Henjō]
# info: found duplication [Sechs_beste_Waka-Dichter]
