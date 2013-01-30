#!/usr/bin/env python
#
# Copyright (C) 2012 Yamauchi, Hitoshi
#
# SVG coordinate extractor
#
"""
\file
\brief SVGcoordsExtractor test
"""

import SVGcoordsExtractor
import unittest

class TestSVGcoordsExtractor(unittest.TestCase):
    """test: SVGcoordsExtractor test."""

    def test_graphextractor(self):
        """test graph (adjacent matrix) extractor."""
        graphfetcherdir   = '/home/hitoshi/data/project/shitohichi-tools/graphfetcher/'
        input_rpath       = 'svgtool/'
        output_rpath      = 'svgtool/'
        input_list_fname  = 'packmaze.svg'
        output_coords_fname = '00test.coords'
        input_fullpath    = graphfetcherdir + input_rpath
        output_fullpath   = graphfetcherdir + output_rpath
        print '\n# input  [' + input_fullpath  + '], filename[' + input_list_fname  + ']'
        print '\n# output path [' + output_fullpath + ']'
        print '# filename [' + output_coords_fname + ']'

        # options
        opt_dict = {}

        ge = SVGcoordsExtractor.SVGcoordsExtractor(opt_dict)
        ge.get_svg_coords(input_fullpath,  input_list_fname,
                          output_fullpath, output_coords_fname)

#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestSVGcoordsExtractor)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)


