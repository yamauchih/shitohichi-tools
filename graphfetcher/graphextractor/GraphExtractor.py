#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Yamauchi, Hitoshi
# For Rebecca from Hitoshi the fool
#
# Graph extractor:
# Get a list of pair {URL, Val} and generate adjacent matrix between URLs.
#
# wget download web page has already been changed the url. I think all
# the pages are in one directory. (Assumption)
#

import os, sys
import urllib
import urllib2
import codecs
from bs4 import BeautifulSoup

class GraphExtractor(object):
    """Extract graph structure from a web pages.
    An adjacent matrix is generated."""

    def __init__(self, _test_url_list):
        """constructor
        \param[in] _test_url_list if None, only analyze this list URL
        """
        sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

        # index to url map. list implementation
        self.__index_to_url_map = []
        # url to index map. dict implementation
        self.__url_to_index_map = {}

        # test URL list
        if _test_url_list == None:
            self.__test_url_list = []
        else:
            self.__test_url_list = _test_url_list

        # current working directory
        self.__cwd = u'./'

        # adjacent matrix: list of [index list], idx -> [index list]
        self.__M_ij = []


    def __load_input_vector(self, _input_vector_list_fname):
        """load input vector. The input file should be created by
        ListFetcher.  Store the input vector in a bijection map
        (a forward map and a backword map).

        \param[in] _input_vector_list_fname input vector list file name (current directory)
        """
        infile = codecs.open(_input_vector_list_fname, mode='r', encoding='utf-8')
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

        # initialize adjacent matrix
        for i in xrange(0, len(self.__index_to_url_map)):
            self.__M_ij.append([])


    def __get_one_page_connectivity(self, _url):
        """get one page connectivity
        \param[in] _url page URL
        """
        file_url = u'file://' + self.__cwd + _url
        # print file_url
        data = urllib2.urlopen(file_url).read()
        soup = BeautifulSoup(data)
        src_link_list = soup.find_all('a')
        dst_link_list = []
        for link in src_link_list:
            dst = link.get('href')
            # print dst
            if (self.__url_to_index_map.has_key(dst)):
                # Show connection
                # print u'connect [' + _url + u']->[' + dst + u']'

                # no duplication test, unordered. But just use
                # set(dst_link_list) solved them
                dst_link_list.append(self.__url_to_index_map[dst])

        # record the list
        idx = self.__url_to_index_map[_url]
        self.__M_ij[idx] = dst_link_list
        # FIXME: not exclude itself and duplicated links
        rec_links = len(dst_link_list)
        # print _url + u' has ' + str(rec_links) + u' recognizable links.'
        return rec_links


    def __get_all_connectivity(self):
        """get all connectivity

        if self.__test_url_list has entries, use that entries for
        test, else analyze all url in the input vector.
        """
        if (len(self.__test_url_list) > 0):
            # test mode
            for url in self.__test_url_list:
                rec_link_count = self.__get_one_page_connectivity(url)
                print u'analyzed [' + url + u'] found ' + str(rec_link_count) +\
                    u' links.'
                if (rec_link_count == 0):
                    print u'Warning! ' + url + u' has no recognizable links. Check the URL input.'
        else:
            cur_i = 0
            total_len_str = str(len(self.__index_to_url_map))
            for url in self.__index_to_url_map:
                cur_i = cur_i + 1
                rec_link_count = self.__get_one_page_connectivity(url)
                print u'analyzed [' + url + u'] ' + str(cur_i) + u'/' + total_len_str +\
                    u' found ' + str(rec_link_count) + u' links.'
                if (rec_link_count == 0):
                    print u'Warning! ' + url + u' has no recognizable links. Check the URL input.'


    def __output_adjacent_matrix(self, _output_fname):
        """output adjacent matrix
        \param[in] _output_fname output filename
        """
        outfile = codecs.open(_output_fname, mode='w', encoding='utf-8')
        outfile.write('# adjacent matrix generated by GraphExtractor by Hitoshi\n')
        outfile.write(str(self.__M_ij) + '\n')


    def get_adjacebt_matrix(self, _working_directory, _input_vector_list_fname, _output_fname):
        """get adjacent matrix
        \param[in] _working_directory working directory to cd
        \param[in] _input_vector_list_fname input vector list file name
        \param[in] _output_fname output file name
        """
        os.chdir(_working_directory)
        self.__cwd = _working_directory
        self.__load_input_vector(_input_vector_list_fname)
        self.__get_all_connectivity()
        self.__output_adjacent_matrix(_output_fname)


if __name__=="__main__":
    print 'Usage: test_graphextractor.py'