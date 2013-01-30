#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Yamauchi, Hitoshi
# For Rebecca from Hitoshi the fool
#
# fix utf8 corruption.
#
# It seems some wget conversion has a problem to put into sometimes
# an illegal utf-8 sequences. Filter that out.
#

import os, sys
import codecs

class FixUtf8File(object):
    """Fix utf-8 file corruption caused by (maybe) wget"""

    def __init__(self, _opt_dict):
        """constructor

        Options:

        - 'error_handling': string. same as codecs.open()'s
          errors. {'strict', 'replace', 'ignore'}
        \param[in] _opt_dict options
        """
        # error_handling
        self.__encoding_errors = 'strict';
        if (_opt_dict.has_key('encoding_errors')):
            self.__encoding_errors = _opt_dict['encoding_errors']
        print u'# Option: encoding_errors:', str(self.__encoding_errors)


    def fix_one_file(self, _inpath, _outfpath):
        """
        fix one utf-8 file
        \param[in] _inpath   input path
        \param[in] _outfpath output path
        """
        fin = codecs.open(_inpath, mode='r', encoding='utf-8', errors=self.__encoding_errors)
        intxt = fin.read()
        fin.close()

        fout = codecs.open(_outfpath, encoding='utf-8', mode='w')
        fout.write(intxt)
        fout.close()
        print u'converted [' + _inpath + u']->[' + _outfpath + u']'


    def fix_all_file(self, _input_dir, _output_dir):
        """fix all files in the input directory.
        \param[in] _input_dir   input files' directory
        \param[in] _output_dir  output files' directory
        """
        if (not os.path.exists(_input_dir)):
            raise StandardError, ('No such input directory [' + _input_dir + ']')
        if (not os.path.exists(_output_dir)):
            raise StandardError, ('No such output directory [' + _output_dir + ']')

        os.chdir(_input_dir)
        for fname in os.listdir("."):
            if (not os.path.isfile(fname)):
                continue
            ufname = unicode(fname, encoding='utf-8', errors='strict')
            outfpath = os.path.join(_output_dir, ufname)
            self.fix_one_file(ufname, outfpath)


if __name__=="__main__":
    print 'Usage: test_fixutf8file.py'

