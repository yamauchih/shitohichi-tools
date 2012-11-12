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
from ILog import ILog

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

        # result
        self.__reduced_author_vec = []

        # Options
        self.__opt_dict   = _opt_dict

        if (_opt_dict.has_key('log_level')):
            ILog.set_output_level_with_dict(_opt_dict)
        ILog.info(u'Option: log_level: ' + str(ILog.get_output_level()))

        # is_enable_stdout_utf8_codec
        if (_opt_dict.has_key('is_enable_stdout_utf8_codec')):
            if(_opt_dict['is_enable_stdout_utf8_codec'] == True):
                sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
                ILog.info(u'Option: is_enable_stdout_utf8_codec: True')
            else:
                ILog.info(u'Option: is_enable_stdout_utf8_codec: False')

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
        if ((len(header_token) < 2)              or # should be 2
            (header_token[0] != '#AuthorVector') or # header keyword
            (header_token[1] != '0')):              # version number
            # This is not a author vector.
            raise StandardError('Error: The file [' + str(_input_vector_fpath) +
                                '] does not match an author vector file header.')
        else:
            ILog.info('check the input author vector file header... pass.')

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
        ILog.info('number of entries: ' + str(len(self.__index_to_author_map)))


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
            ILog.info('check the pagerank data file header... pass.')

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


    def __gen_reduce_author_vec(self):
        """generate reduced (removed source/sink nodes)
        """
        assert(len(self.__reduced_author_vec) == 0) # not yet generated
        assert(len(self.__data_result_idx) > 0)     # the data should have been loaded.

        for valid_author_idx in self.__data_result_idx:
            adjusted_idx = valid_author_idx - 1
            assert(adjusted_idx >= 0)
            self.__reduced_author_vec.append(self.__index_to_author_map[adjusted_idx])
            # print valid_author_idx, self.__index_to_author_map[adjusted_idx]

        # print len(self.__reduced_author_vec), len(self.__data_result_idx)
        assert(len(self.__reduced_author_vec) == len(self.__data_result_idx))

        # if save the self.__reduced_author_vec here, reduced map only


    def __save_result(self, _author_vec_fname, _data_fname, _save_fname):
        """save the result to _save_fname.
        \param[in] _author_vec_fname input author vector file name (for the header only)
        \param[in] _data_fname       input pagerank data file name (for the header only)
        \param[in] _save_fname save  save file name
        """
        try:
            # open output file with utf-8 codec
            outfile = codecs.open(_save_fname, mode='w', encoding='utf-8')

            # header
            outfile.write(u'#Remapper 0\n')
            outfile.write(u'# -*- coding: utf-8 -*-\n')
            outfile.write(u'#\n')
            outfile.write(u'# generated by Remapper. (C) Hitoshi 2012\n')
            outfile.write(u'# input vector file [' + _author_vec_fname + ']\n')
            outfile.write(u'# input data file   [' + _data_fname       + ']\n')
            outfile.write(u'#\n')

            # print out pagerank sorted vector
            for pgsorted_idx in self.__data_sorted_pidx :
                adjusted_idx = pgsorted_idx - 1
                assert(adjusted_idx >= 0)
                outfile.write(self.__reduced_author_vec[adjusted_idx] + '    ' + \
                              str(self.__data_pagerank[adjusted_idx]) + '\n')

            outfile.close()

        except IOError as e:
            print "error! Remapper.__save_result(): I/O error({0}): {1}".format(e.errno, e.strerror)
            sys.exit(1)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    def remap_author(self, _author_vec_fname, _data_fname, _save_fname):
        """remap the author list according to the pagerank result data

        \parm[in] _author_vec_fname author vector filename (usually UTF-8 file)
        \parm[in] _data_fname       pagerank result data file
        \parm[in] _save_fname       save result filename
        """
        ILog.info(u'input vector file     [' + _author_vec_fname + u']')
        ILog.info(u'input rankdata file   [' + _data_fname       + u']')
        ILog.info(u'output rankedata file [' + _save_fname       + u']')

        self.__load_input_vector(_author_vec_fname)
        self.__read_data_file(_data_fname)

        self.__gen_reduce_author_vec()

        # print out reduced vector
        # for valid_author in self.__reduced_author_vec:
        #     print valid_author

        self.__save_result(_author_vec_fname, _data_fname, _save_fname)


if __name__=="__main__":

    print u'# Usage: run the test_remapper_en_en_0.py.'
