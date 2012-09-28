#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Yamauchi, Hitoshi
#
# LinkVectorExtractor test: de_de (Deutsche Writer in Deutsche Wiki)
#
"""
\file
\brief LinkVectorExtractor test: de_de (Deutsche Writer in Deutsche Wiki)
"""

import os
import LinkVectorExtractor
import unittest

class TestLinkVectorExtractor(unittest.TestCase):
    """test: LinkVectorExtractor test."""

    def test_linkvectorextractor(self):
        """test generate URL list by List of Deutsche from Deutsche wiki (de_de).
        The export encoding option 'ascii' gives you matlab readable author vector.
        """
        # print u'# Need LC_ALL setting to utf-8, e.g., en_US.utf-8, ja_JP.utf-8.'
        graphfetcherdir = u'/home/hitoshi/data/project/shitohichi-tools/graphfetcher/'

        input_rpath       = u'data/german_writer/de.wikipedia.org/wiki/'

        # if substring of the following list matches the href, ignore.
        ignore_href_list = [
            'w/index.php', 'Kategory', '/wiki', 'Wikipedia:', 'Portal',
            'Liste_von_Autoren', 'Spezial', 'Hilfe', 'Diskussion'
            ]

        author_root_fname = u'Liste_deutschsprachiger_Schriftsteller'
        # Liste_deutschsprachiger_Schriftsteller/[A-Z], except 'X' and 'Y'
        author_first_char_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                                  'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                                  'W', 'Z' ]

        output_rpath      = u'data/german_writer/de.wikipedia.org/'
        outdir = os.path.join(graphfetcherdir, output_rpath)

        output_list_basename = u'de_de_writer'

        optdict = {'export_encoding': 'utf-8'}
        # optdict = {'export_encoding': 'ascii'}
        # optdict = {'export_encoding': 'shift-jis'}

        # what tag have the links?
        optdict['tag_in_each_link'] = 'li'

        output_list_fname = output_list_basename + '.' + optdict['export_encoding'] + '.vector'
        output_full_path = os.path.join(outdir, output_list_fname)
        lf = LinkVectorExtractor.LinkVectorExtractor(ignore_href_list, optdict)

        for prefix_ch in author_first_char_list:
            indir = os.path.join(graphfetcherdir, input_rpath)
            input_fullpath_dir = os.path.join(indir, author_root_fname)
            input_fullpath     = os.path.join(input_fullpath_dir, prefix_ch)
            root_url    = u'file:///' + input_fullpath
            print u'# input [' + root_url    + u']'
            lf.get_link_list(root_url)

        print u'# export [' + output_full_path + u']'
        lf.export_to_file(output_full_path)


#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestLinkVectorExtractor)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)

# Duplication list
#

