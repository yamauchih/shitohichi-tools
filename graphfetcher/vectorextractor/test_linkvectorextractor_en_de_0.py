#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012-2013 Yamauchi, Hitoshi
#
# LinkVectorExtractor test: en_de (English Writer, German Wiki)
#
"""
\file
\brief LinkVectorExtractor test: en_de (English Writer, German Wiki)
"""

import os
import LinkVectorExtractor
import unittest, filecmp

class TestLinkVectorExtractor(unittest.TestCase):
    """test: LinkVectorExtractor test."""

    def linkvectorextractor(self, _opt_dict):
        """test generate URL list by List of English writers from
        German wiki (en_de).  The export encoding option 'ascii'
        gives you matlab readable author vector.
        """
        # print u'# Need LC_ALL setting to utf-8, e.g., en_US.utf-8, ja_JP.utf-8.'
        graphfetcherdir = u'/home/hitoshi/data/project/shitohichi-tools/graphfetcher/'

        input_rpath       = u'data/english_writer/de.wikipedia.org/wiki/'
        author_root_fname = u'Liste_britischer_Schriftsteller'

        indir = os.path.join(graphfetcherdir, input_rpath)
        input_fullpath = os.path.join(indir, author_root_fname)
        root_url    = u'file:///' + input_fullpath

        output_rpath         = u'data/english_writer/de.wikipedia.org/'
        output_list_basename = u'en_de_writer'
        outdir = os.path.join(graphfetcherdir, output_rpath)

        print
        print u'# input [' + root_url    + u']'
        # if substring of the following list matches the href, ignore.
        # If exact match filter is needed, use blacklistset option.
        ignore_href_list = [
            '../w/index.php', 'Category', '/wiki', 'Wikipedia:', 'Portal',
            'List_of_German-language_philosophers',
            'List_of_German-language_playwrights',
            'List_of_German-language_poets',
            'Liste_englischsprachiger_Schriftsteller',
            'Liste_amerikanischer_Schriftsteller',
            'Liste_kanadischer_Schriftsteller',
            'Liste_australischer_Schriftsteller',
            'Liste_irischer_Schriftsteller',
            'Liste_schottischer_Schriftsteller',
            'Autoren_von_Kinder-_und_Jugendliteratur',
            'Kategorie:',
            'Liste_britischer_Schriftsteller',
            '/w/index.php?title=Spezial:Buch&bookcmd',
            '/w/index.php?title=Liste_britischer_Schriftsteller&printable=yes',
            'Spezial:Letzte_?nderungen',
            'Spezial:Linkliste/Liste_britischer_Schriftsteller',
            'Spezial:Spezialseiten',
            u'Spezial:Zufällige_Seite',
            u'Hilfe:Übersicht',
            u'Spezial:Letzte_Änderungen'
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

        # indir = os.path.join(graphfetcherdir, input_rpath)
        # input_fullpath = os.path.join(indir, author_root_fname)
        # root_url    = u'file:///' + input_fullpath

        # print u'# input [' + root_url    + u']'
        # lf.get_link_list(root_url)

        # print u'# export [' + output_full_path + u']'
        # lf.export_to_file(output_full_path)

#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestLinkVectorExtractor)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)

# Duplication list
#
# info: found duplication [George_Mackay_Brown]
# info: found duplication [William_Sharp]
