#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Yamauchi, Hitoshi
# For Rebecca from Hitoshi the fool
#
#
# generate author vector for cross ranking.
#

import os, sys, codecs
from ILog import ILog

class GenAuthorVector(object):
    """Generate author vector from AuthorRankVector file.
    This is simple filter. Check the header and print out $1.
    """

    def __init__(self, _opt_dict):
        """constructor
        Currently, no option.
        \param[in] _opt_dict          option dict
        """
        self.__opt_dict = _opt_dict

    def run_filter(self, _in_ar_vec_fpath, _out_a_vec_fpath):
        """run filter
        \param[in] _in_ar_vec_fpath input author pagerank vector file full path
        \param[in] _out_a_vec_fpath output author vector file full path
        """
        try:
            infile  = codecs.open(_in_ar_vec_fpath, mode='r', encoding='utf-8')
            outfile = codecs.open(_out_a_vec_fpath, mode='w', encoding='utf-8')

            # Check the file header.
            header_line  = infile.readline()
            header_token = header_line.split()
            if ((len(header_token) < 2)                  or # should be 2
                (header_token[0] != '#AuthorRankVector') or # header keyword
                (header_token[1] != '0')):                  # version number
                # This is not a author vector.
                raise StandardError('Error: The file [' + str(_in_ar_vec_fpath) +
                                    '] does not match an author rank vector file header.')
            else:
                ILog.info('check the input author rank vector file header... pass.')


            outfile.write(u'#AuthorVector 0\n')
            outfile.write(u'#\n')
            outfile.write(u'# Author vector\n')
            outfile.write(u'# -*- coding: utf-8 -*-\n')
            outfile.write(u'#\n')
            outfile.write(u'# generated by GenAuthorVector. (C) Hitoshi 2012\n')
            outfile.write(u'# input vector file [' + _in_ar_vec_fpath + ']\n')
            outfile.write(u'# input data file   [' + _out_a_vec_fpath + ']\n')
            outfile.write(u'#\n')

            for fline in infile:
                line = fline.strip()
                if ((len(line) > 0) and (line[0] != '#')):
                    line_token_list = line.split()
                    assert(len(line_token_list) > 0)
                    outfile.write(line_token_list[0] + '\n')

            infile. close()
            outfile.close()

        except IOError as e:
            print "error! Remapper.__save_result(): I/O error({0}): {1}".\
                  format(e.errno, e.strerror)
            sys.exit(1)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise



if __name__=="__main__":
    print u'# Usage: run the test_gen_author_vector_0.py.'

