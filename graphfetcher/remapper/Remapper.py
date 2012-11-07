#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Yamauchi, Hitoshi
# For Rebecca from Hitoshi the fool
#
# matlab/octave can not handle UTF-8 data in a convenient way.
# Therefore, I need to remap the result.
#
# I need two mapping.
#  - original authoer vector -> removed sink/source author vector
#  - removed sink/source author vector -> pagerank permutation vector
# This program does both mapping.
#

import os, sys, codecs

class Remapper(object):
    """Remap
    - the input vector to removed sink/source author vector (UTF-8 author vector)
    - removed sink/source author vector to pagerank permutation vector.
    """

    def __init__(self, _opt_dict):
        """constructor
        \param[in] _opt_dict          option dict
        """

        # index to author map. list implementation
        self.__index_to_author_map = []
        # author to index map. dict implementation
        self.__author_to_index_map = {}

        # data entry lists
        #     result_index, pagerank, sorted_permulation_index
        self.__data_result_idx  = []
        self.__data_pagerank    = []
        self.__data_sorted_pidx = []

        # Options
        self.__opt_dict   = _opt_dict

        self.__log_level = 2
        if (_opt_dict.has_key('log_level')):
            self.info_out(u'# Option: log_level: ' + str(_opt_dict['log_level']))
            self.__log_level = _opt_dict['log_level']
        else:
            self.info_out(u'# Option: log_level: ' + str(self.__log_level))


    def error_out(self, _mes):
        """errlr level log output"""
        if(self.__log_level == 0):
            print u'error:', _mes

    def info_out(self, _mes):
        """info level log output"""
        if(self.__log_level >= 1):
            print u'info:', _mes

    def debug_out(self, _mes):
        """debug level log output"""
        if(self.__log_level >= 2):
            print u'debug:', _mes


    def __print_str(self, _str):
        """convenient function for print unicode or string using utf-8
        without casting exception.
        \param[in] _str type unicode or type str.
        """
        if type(_str) == type(u'a'):
            sys.stdout.write(_str.encode('utf-8', 'replace') + '\n')
        else:
            sys.stdout.write(_str + '\n')


    def __load_input_vector(self, _input_vector_fpath):
        """load input vector. The input file should be created by
        LinkVectorExtractor.  Store the input vector in a list.

        Similar to the GraphExtractor's _load_input_vector(). The data
        destination differs.

        \param[in] _input_vector_fpath input vector list file name, fullpath
        """
        infile = codecs.open(_input_vector_fpath, mode='r', encoding='utf-8')

        # Check the file header.
        header_line  = infile.readline()
        header_token = header_line.split()
        if ((len(header_token) < 2)                     or # should be 2
            (header_token[0] != '#LinkVectorExtractor') or # header keyword
            (header_token[1] != '0')):                     # version number
            # This is not a author vector.
            raise StandardError('Error: The file [' + str(_input_vector_fpath) +
                                '] does not match an author vector file header.')
        else:
            self.info_out('check the input author vector file header... pass.')

        idx = 0
        for fline in infile:
            line = fline.strip()
            if ((len(line) > 0) and (line[0] != '#')):
                # non null and not started # line ... add to the map
                if (not self.__author_to_index_map.has_key(line)):
                    self.__author_to_index_map[line] = idx
                    self.__index_to_author_map.append(line)
                    idx = idx + 1
                else:
                    # duplication should not be allowed for graph extraction.
                    raise StandardError('Error: duplication found [' + str(line) + '] at ' + str(idx))

        assert len(self.__author_to_index_map) == len(self.__index_to_author_map)
        self.info_out('number of entries: ' + str(len(self.__index_to_author_map)))


    def __read_data_file(self, _data_fname):
        """read pagerank data file name
        \param[in] _data_fname data file path name
        """
        infile = codecs.open(_data_fname, mode='r', encoding='ascii')

        # Check the file header.
        header_line  = infile.readline()
        header_token = header_line.split()
        if ((len(header_token) < 2)              or # should be 2
            (header_token[0] != '#PageRankData') or # header keyword
            (header_token[1] != '0')):              # version number
            # This is not a author vector.
            raise StandardError('Error: The file [' + str(_data_fname) +
                                '] does not match a pagerank data file header.')
        else:
            self.info_out('check the pagerank data file header... pass.')

        # result_index pagerank sorted_permulation_index
        for fline in infile:
            line = fline.strip()
            if (line[0] == '#'):
                continue

            num = line.split(' ')

            assert(len(num) == 3)
            # three data at a line
            # print 'data: ', num, num[0], num[1], num[2]
            self.__data_result_idx .append(int  (num[0]))
            self.__data_pagerank   .append(float(num[1]))
            self.__data_sorted_pidx.append(int  (num[2]))


    def remap_author(self, _author_vec_fname, _data_fname):
        """remap the author list according to the pagerank result data

        \parm[in] _author_vec_fname author vector filename (usually UTF-8 file)
        \parm[in] _data_fname       pagerank result data file
        """
        self.__load_input_vector(_author_vec_fname)
        self.__read_data_file(_data_fname)



if __name__=="__main__":

    print u'# Usage: run the test_remapper_en_en_0.py.'
