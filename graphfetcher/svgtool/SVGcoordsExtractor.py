#!/usr/bin/env python
#
# Copyright (C) 2012 Yamauchi, Hitoshi
#
# SVG coordinate extractor
#

import os, sys
import urllib
import urllib2
import codecs
from bs4 import BeautifulSoup

class SVGcoordsExtractor(object):
    """Extract SVG line coordinates."""

    def __init__(self, _opt_dict):
        """constructor

        Options:

        \param[in] _opt_dict options
        """
        self.__scaling = 0.01


    def __output_path(self, _path_list):
        """output line path list
        \param[in] _path_list path list of SVG data
        """
        for path in _path_list:
            # M 0,1 L 10,20 30,40 -> ['M' '0,1' 'L' '10,20' '30,40']
            coord_str_list = path['d'].split()
            assert coord_str_list[0] == 'M', 'the element [0] is not M in the path'
            assert coord_str_list[2] == 'L', 'the element [2] is not L in the path'
            coord_list = []
            coord_list.append(coord_str_list[1])
            coord_list.extend(coord_str_list[3:])
            print 'path_segment:'
            for coord in coord_list:
                xy = coord.split(',')
                assert len(xy) == 2, 'xy coodinate should have x and y'
                # print as xy
                x = self.__scaling * float(xy[0])
                y = self.__scaling * float(xy[1])
                print str(x) + ', ' + str(y)


    def __output_rect(self, _rect_list):
        """output rect as a line segments
        \param[in] _rect_list rectangle list of SVG data
        """
        for rect in _rect_list:
            x = self.__scaling * float(rect['x'])
            y = self.__scaling * float(rect['y'])
            w = self.__scaling * float(rect['width'])
            h = self.__scaling * float(rect['height'])
            print 'rect_segment:'
            print str(x)     + ', ' + str(y)
            print str(x + w) + ', ' + str(y)
            print str(x + w) + ', ' + str(y + h)
            print str(x)     + ', ' + str(y + h)
            print str(x)     + ', ' + str(y)


    def __parse_svg_file(self, _url):
        """get one page connectivity
        \param[in] _url page URL
        """
        file_url = u'file://' + self.__cwd + _url
        # print file_url
        data = urllib2.urlopen(file_url).read()
        soup = BeautifulSoup(data)
        # pretty print only
        # print (soup.prettify(formatter="html"))

        # path
        path_list = soup.find_all('path')
        self.__output_path(path_list)

        # rectangle
        rect_list = soup.find_all('rect')
        self.__output_rect(rect_list)


    def get_svg_coords(self,
                       _working_directory, _input_fname,
                       _output_directory,  _output_fname):
        """get adjacent matrix
        \param[in] _working_directory working directory to cd, input html directory.
        \param[in] _input_fname input svg file name
        \param[in] _output_directory  output directory
        \param[in] _output_fname output coordinates file name
        """
        os.chdir(_working_directory)
        self.__cwd = _working_directory
        self.__output_dir = _output_directory
        self.__parse_svg_file(_input_fname)



if __name__=="__main__":
    print 'Usage: test_svgcoordsextractor_0.py'
