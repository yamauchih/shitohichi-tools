#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Yamauchi, Hitoshi
# For Rebecca from Hitoshi the fool
#
# report the cross ranking from the author vector set
#

import os, sys, re, math
import codecs
from ILog import ILog

class CrossRank(object):
    """Report the cross ranking result."""

    def __init__(self, _opt_dict):
        """constructor

        Options:

        - 'log_level': int
        See ILog.

        - 'base_fpath': str
        input file full path for the base data. All the lines are in
        the output.

        - 'ref_fpath': str
        reference file full path.

        - 'out_fpath': str
        output file full path.

        - 'is_tex_umlaut': bool
        When True, umlaut charactor is converted with TeX style, e.g., ü -> \"{u}.
        default: False

        - 'is_tex_table': bool
        When True, separator becomes & for TeX table.
        default: False

        - 'is_add_line_number': bool
        When True, line number is added.
        default: False

        - 'is_rank_out': bool
        When True, the refernce file's rank number is the
        result. Otherwise, <found>. The <found> for finding the person
        on the list. Usecase is to show who is the Nobel prize winner
        to show.
        default: True

        - 'is_enable_stdout_utf8_codec': bool
        default: False

        Example:
        If the base file is:

          Johann_Wolfgang_von_Goethe
          Friedrich_Schiller
          Johann_Christoph_Gottsched
          Thomas_Mann

        If the reference file is:

          Friedrich_Schiller
          Johann_Christoph_Gottsched
          Johann_Wolfgang_von_Goethe
          Thomas_Mann

        Then output will be

          Johann_Wolfgang_von_Goethe   3
          Friedrich_Schiller           1
          Johann_Christoph_Gottsched   2
          Thomas_Mann                  4

        Tips:
          - You may process the input file with gawk '{print $1}'
          infile, to get your interesting column of the file, for
          instance.

          - unix paste command concatinate the columns

        \param[in] _opt_dict options
        """

        # option handling
        if (_opt_dict.has_key('log_level')):
            ILog.set_output_level_with_dict(_opt_dict)
        ILog.info(u'Option: log_level: ' + str(ILog.get_output_level()))

        if ('base_fpath' not in  _opt_dict):
            raise StandardError, ('base_fpath is not specified.')

        if ('ref_fpath' not in  _opt_dict):
            raise StandardError, ('ref_fpath is not specified.')

        self.__base_fpath = _opt_dict['base_fpath']
        ILog.info(u'Option: base_fpath: ' + self.__base_fpath)

        self.__ref_fpath  = _opt_dict['ref_fpath']
        ILog.info(u'Option: ref_fpath: ' + self.__ref_fpath)

        self.__out_fpath  = '-'
        if ('out_fpath' in  _opt_dict):
            self.__out_fpath  = _opt_dict['out_fpath']
        ILog.info(u'Option: out_fpath: ' + self.__out_fpath)

        self.__is_tex_umlaut = False
        if ('is_tex_umlaut' in  _opt_dict):
            self.__is_tex_umlaut = _opt_dict['is_tex_umlaut']
        ILog.info(u'Option: is_tex_umlaut: ' + str(self.__is_tex_umlaut))

        self.__is_tex_table = False
        if ('is_tex_table' in  _opt_dict):
            self.__is_tex_table  = _opt_dict['is_tex_table']
        ILog.info(u'Option: is_tex_table: ' + str(self.__is_tex_table))

        self.__is_add_line_number = False
        if ('is_add_line_number' in  _opt_dict):
            self.__is_add_line_number = _opt_dict['is_add_line_number']
        ILog.info(u'Option: is_add_line_number: ' + str(self.__is_add_line_number))

        self.__is_rank_out = True
        if ('is_rank_out' in  _opt_dict):
            self.__is_rank_out = _opt_dict['is_rank_out']
        ILog.info(u'Option: is_rank_out: ' + str(self.__is_rank_out))

        # is_enable_stdout_utf8_codec
        if ('is_enable_stdout_utf8_codec' in _opt_dict):
            if(_opt_dict['is_enable_stdout_utf8_codec'] == True):
                sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
                ILog.info(u'Option: is_enable_stdout_utf8_codec: True')
            else:
                ILog.info(u'Option: is_enable_stdout_utf8_codec: False')

        self.__opt_dict = _opt_dict

        # base author list
        self.__base_author_list = []
        # ref  author name -> rank map
        self.__ref_author_rank_map = {}
        # max author name length
        self.__max_author_name_len = 0

        # precompiled regex for search and replace
        self.__re_uml_A   = re.compile(u'Ä', re.UNICODE)
        self.__re_uml_a   = re.compile(u'ä', re.UNICODE)
        self.__re_uml_O   = re.compile(u'Ö', re.UNICODE)
        self.__re_uml_o   = re.compile(u'ö', re.UNICODE)
        self.__re_uml_U   = re.compile(u'Ü', re.UNICODE)
        self.__re_uml_u   = re.compile(u'ü', re.UNICODE)
        self.__re_szet    = re.compile(u'ß', re.UNICODE)
        self.__re_uml_all = re.compile(u'[ÄäÖöÜüß]', re.UNICODE)


    def __load_file(self):
        """load base and ref files"""
        # open base file with utf-8 codec
        try:
            # read the author list
            basefile = codecs.open(self.__base_fpath, mode='r', encoding='utf-8')
            for fline in basefile:
                line = fline.strip()
                if ((len(line) > 0) and (line[0] == '#')):
                    continue            # skip the comment line

                self.__base_author_list.append(line)

            # read the reference list
            reffile  = codecs.open(self.__ref_fpath,  mode='r', encoding='utf-8')
            ref_rank_num = 1
            for fline in reffile:
                line = fline.strip()
                if ((len(line) > 0) and (line[0] == '#')):
                    continue            # skip the comment line
                self.__ref_author_rank_map[line] = ref_rank_num
                ref_rank_num = ref_rank_num + 1

        except IOError as (errno, strerror):
            print "# I/O error({0}): {1}".format(errno, strerror)
            print '# Also you need LC_ALL setting to utf-8, e.g., en_US.utf-8, ja_JP.utf-8.'
            print '# Do input files exist?', self.__base_fpath, self.__ref_fpath


    def __out_tex_table_sep(self, _outfile):
        """output tex table separator if enabled
        \param[in] _outfile output file (stream)"""

        if (self.__is_tex_table):
            _outfile.write('& ')


    def __out_refrank(self, _refrank, _outfile):
        """output reference rank according to the __is_rank_out status.
        \param[in] _outfile output file (stream)"""

        if (self.__is_rank_out):
            _outfile.write(str(_refrank))
        else:
            if (_refrank > 0):
                _outfile.write(u'<found>')
            else:
                _outfile.write(u'<na>')


    def __out_line_number(self, _line_number, _outfile):
        """output line number if enabled.
        \param[in] _line_number line number to output
        \param[in[ _outfile output file (stream)"""

        if (not self.__is_add_line_number):
            return

        # A hack. But I think we will not analyze more than 999999
        # people.
        max_digit = 6
        use_digit = int(math.log10(_line_number))
        num_digit = max_digit - use_digit
        if (num_digit < 0):
            num_digit = 0
        _outfile.write(str(_line_number) + (' ' * num_digit))
        self.__out_tex_table_sep(_outfile)

    def __out_author_name(self, _author_str, _outfile):
        """output author name. If is_tex_umlaut on, process the umlaut
        charactors

        \param[in] _author_str author name string
        \param[in[ _outfile output file (stream)"""

        if (self.__is_tex_umlaut):
            # s = u'AE = Ä, ae = ä, OE = Ö, oe = ö, UE = Ü, ue = ü, ss = ß'
            if(self.__re_uml_all.search(_author_str) != None):
                _author_str = self.__re_uml_A.sub(u'\\"{AE}', _author_str)
                _author_str = self.__re_uml_a.sub(u'\\"{ae}', _author_str)
                _author_str = self.__re_uml_O.sub(u'\\"{OE}', _author_str)
                _author_str = self.__re_uml_o.sub(u'\\"{oe}', _author_str)
                _author_str = self.__re_uml_U.sub(u'\\"{UE}', _author_str)
                _author_str = self.__re_uml_u.sub(u'\\"{ue}', _author_str)
                _author_str = self.__re_szet .sub(u'{\\ss}',  _author_str)

            pack_space_num = (self.__max_author_name_len - len(_author_str))
            if (pack_space_num < 1):
                pack_space_num = 1      # in case there are a few umlauts
            _outfile.write(_author_str + (u' ' * pack_space_num))


    def __print_out_cross_rank(self):
        """print out the cross rank with looking up the map
        """
        # open the output file
        outfile = codecs.open(self.__out_fpath, mode='w', encoding='utf-8')

        # get the max column (author name) length of the base
        max_col_len = 0
        for i in self.__base_author_list:
            cur_col_len = len(i)
            if max_col_len < cur_col_len:
                max_col_len = cur_col_len

        self.__max_author_name_len = max_col_len
        if (self.__is_tex_umlaut):
            # A hack. If one umlaut in the name, this +4 (ü -> \"{u})
            # works, but if a name has more than two umlaut
            # charactors, then this should be +8. Depends on the how
            # many umlaut and ss. Here, just assume one.
            self.__max_author_name_len = self.__max_author_name_len + 4


        # get the max column length of the base
        line_number = 1
        for aut in self.__base_author_list:
            # line number
            self.__out_line_number(line_number, outfile)
            line_number = line_number + 1

            # put the author name
            self.__out_author_name(aut, outfile)
            self.__out_tex_table_sep(outfile)

            # put the refrank
            refrank = -1                # not exist
            if (aut in self.__ref_author_rank_map):
                refrank = self.__ref_author_rank_map[aut]
            self.__out_refrank(refrank, outfile)

            outfile.write('\n')


    def show_cross_rank(self):
        """show the cross rank"""
        self.__load_file()
        self.__print_out_cross_rank()



if __name__=="__main__":
    print 'Usage: test_crossrank_0.py'

