#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Yamauchi, Hitoshi
# For Rebecca from Hitoshi the fool
#
# Graph extractor:
# Get a list of pair {URL, Val} and generate adjacent matrix between URLs.
#

import os, sys
import urllib
import urllib2
import codecs
from bs4 import BeautifulSoup

class GraphExtractor(object):
    """Extract graph structure from a web pages.
    An adjacent matrix is generated."""

    def __init__(self):
        """constructor
        """
        sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

        # index to url map. list implementation
        self.__index_to_url_map = []
        # url to index map. dict implementation
        self.__url_to_index_map = {}


    def __load_input_vector(self, _input_vector_list_path):
        """load input vector. The input file should be created by
        ListFetcher.  Store the input vector in a bijection map
        (a forward map and a backword map).

        \param[in] _input_vector_list_path input vector list file full path
        """
        infile = codecs.open(_input_vector_list_path, mode='r', encoding='utf-8')
        idx = 0
        for fline in infile:
            line = fline.strip()
            if ((len(line) > 0) and (line[0] != '#')):
                # non null and not started # line ... add to the map
                if (not self.__url_to_index_map.has_key(line)):
                    self.__url_to_index_map[line] = idx
                    self.__index_to_url_map.append(line)
                    idx = idx + 1
                else:
                    print u'duplication found [' + line + u']' + ' at ' + str(idx) + \
                        u' ignored'

        assert len(self.__url_to_index_map) == len(self.__index_to_url_map)
        print '# number of entries: ', len(self.__index_to_url_map)


    def __get_all_connectivity(self):
        """
        """
        pass

    def __output_adjacent_matrix(self):
        """
        """
        pass


    def get_adjacebt_matrix(self, _input_vector_list_fname, _output_path):
        """get adjacent matrix
        \param[in] _input_vector_list_fname
        \param[in] _output_path
        """
        self.__load_input_vector(_input_vector_list_fname)
        self.__get_all_connectivity()
        self.__output_adjacent_matrix()


if __name__=="__main__":
    print 'Usage: test_graphextractor.py'
