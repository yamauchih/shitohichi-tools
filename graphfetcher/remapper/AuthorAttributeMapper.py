#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012-2013 Yamauchi, Hitoshi
# For Rebecca from Hitoshi the fool
#
# Award mapper
#  - authoer vector <-> award vector map generation
#
# Award vector has entries:
#  Author item_1 item_2 item_3 ...
#
# Example. (akutagawa_winner.vector)
#
# #AuthorAttributeVector 0 MaxAttributeCount 3
# # comment
# # Author  n-th_winner	book_title
# 石川達三  1           蒼氓
# 小田嶽夫  3           城外
# 鶴田知也  3           コシャマイン記
#
# Header structure. The first line of the file.
#
# #AuthorAttributeVector version_number MaxAttributeCount max_attrib_count
#
# #AuthorAttributeVector   header keyword
# version_number           author attribute vector version number (one integer)
# MaxAttributeCount        A file attribute keyword.
# max_attrib_count         The max number of attributes (one integer)
#
import os, sys, codecs
from ILog import ILog

class AuthorAttributeMapper(object):
    """Remap
    - the input vector to removed sink/source author vector (UTF-8 author vector)
    - removed sink/source author vector to pagerank permutation vector.
    """

    def __init__(self, _opt_dict):
        """constructor

        Option key:

        - 'output_attrib_idx' which attribute do you want to map.
        This is an index of the attribute list. So the author
        attribute file has the entry.

           Author        n-th_winner     book_title
           石川達三      1               蒼氓

        In this case, key = '石川達三', value_list = ['1', '蒼氓'].
        Therefore, output_attrib_idx: 0 means output n-th_winner since
        this is the 0th element of value_list.

        \param[in] _opt_dict          option dict
        """

        # author vector list
        self.__author_list = []

        # author to attribute list [n-th_winner, book_title, ] map.
        self.__author_to_attrlist_map = {}

        # attribute list max length. This count includes author entry.
        self.__attrib_list_max_count = 0

        # mapped result list
        self.__mapped_result_list = []

        # Options
        self.__opt_dict   = _opt_dict

        if (_opt_dict.has_key('log_level')):
            ILog.set_output_level_with_dict(_opt_dict)
        ILog.info(u'Option: log_level: ' + str(ILog.get_output_level()))

        if ('output_attrib_idx' not in _opt_dict):
            raise StandardError("option has no 'output_attrib_idx' key.")

        self.__output_attrib_idx = _opt_dict['output_attrib_idx']
        assert self.__output_attrib_idx >= 0
        ILog.info('Option: output_attrib_idx: ' + str(self.__output_attrib_idx))

        # is_enable_stdout_utf8_codec
        # if (_opt_dict.has_key('is_enable_stdout_utf8_codec')):
        #     if(_opt_dict['is_enable_stdout_utf8_codec'] == True):
        #         sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
        #         ILog.info(u'Option: is_enable_stdout_utf8_codec: True')
        #     else:
        #         ILog.info(u'Option: is_enable_stdout_utf8_codec: False')



    def __read_author_attribute_file(self, _author_attrib_fpath):
        """read author attribute vector file.

        \param[in] _author_attrib_fpath input author attribute vector
        file fullpath.
        """
        infile = codecs.open(_author_attrib_fpath, mode='r', encoding='utf-8')

        # Check the file header.
        header_line  = infile.readline()
        header_token = header_line.split()
        if ((len(header_token) < 4)                       or # should be 4
            (header_token[0] != '#AuthorAttributeVector') or # header keyword
            (header_token[1] != '0')                      or # version number
            (header_token[2] != 'MaxAttributeCount')):       # max attribute count
            # This is not a author attribute vector.
            raise StandardError('Error: The file [' + str(_author_attrib_fpath) +
                                '] does not match an author attribute vector file header.')
        else:
            ILog.info('check the input author attribute vector file header... pass.')

        self.__attrib_list_max_count = int(header_token[3])
        if (self.__attrib_list_max_count < 2):
            raise StandardError('Error: MaxAttributeCount [' + header_token[3] +
                                '] should be int and more than 1.')

        idx = 0
        for fline in infile:
            idx += 1
            line = fline.strip()
            if ((len(line) == 0) or (line[0] == '#')):
                # null line or started with #
                continue
            # get attribute list
            columns = line.split()
            col_count = len(columns)
            assert (col_count > 0)

            # Check the duplicate key
            if(columns[0] in self.__author_to_attrlist_map):
                raise StandardError('Error: Duplicate key [' + columns[0] + '] found.')

            self.__author_to_attrlist_map[columns[0]] = columns[1:]

        ILog.info('number of entries: ' + str(len(self.__author_to_attrlist_map)))


    def dump_author_attribute_list_map(self):
        """dump author to attribute list map for debugging."""
        for i in self.__author_to_attrlist_map:
            print i, self.__author_to_attrlist_map[i]


    def __read_author_vector_file(self, _author_vec_fpath):
        """read author vector file
        \param[in] _author_vec_fpath author vector file full path
        """
        infile = codecs.open(_author_vec_fpath, mode='r', encoding='utf-8')

        # Check the file header.
        header_line  = infile.readline()
        header_token = header_line.split()
        if ((len(header_token) < 2)              or # should be 2
            (header_token[0] != '#AuthorVector') or # header keyword
            (header_token[1] != '0')):              # version number
            # This is not a author vector.
            raise StandardError('Error: The file [' + str(_author_vec_fpath) +
                                '] does not match a pagerank data file header.')


        else:
            ILog.info('check the author vector file header... pass.')

        # read authors
        for fline in infile:
            line = fline.strip()
            if (line[0] == '#'):
                continue

            self.__author_list.append(line)


    def __map_attribute(self):
        """map author to attribute"""

        assert (self.__output_attrib_idx < self.__attrib_list_max_count)

        not_found_count = 0
        for i in self.__author_list:
            if (i not in self.__author_to_attrlist_map):
                # ILog.info(u'[' + i + '] is not in author attribute map list.')
                not_found_count += 1
                self.__mapped_result_list.append([i, u''])
            else:
                val_list = self.__author_to_attrlist_map[i]
                assert (self.__output_attrib_idx < len(val_list))
                self.__mapped_result_list.append([i, val_list[self.__output_attrib_idx]])

        ILog.info(str(not_found_count) +\
                  ' authors attributes are not found in the given data file.')



    def __save_result(self, _author_vec_fpath, _author_attrib_fpath, _save_fpath):
        """save the result to _save_fname.
        \param[in] _author_vec_fpath input author vector file fullpath
        \param[in] _author_vec_fpath input author attribute vector file fullpath
        \param[in] _save_fpath       save file fullpath
        """
        try:
            # open output file with utf-8 codec
            outfile = codecs.open(_save_fpath, mode='w', encoding='utf-8')

            # header
            outfile.write(u'#AuthorAttribMap 0\n')
            outfile.write(u'#\n')
            outfile.write(u'# Author and attribute map\n')
            outfile.write(u'# -*- coding: utf-8 -*-\n')
            outfile.write(u'#\n')
            outfile.write(u'# generated by AuthorAttributeMapper. (C) Hitoshi 2012-2013\n')
            outfile.write(u'# input vector file [' + _author_vec_fpath    + ']\n')
            outfile.write(u'# input data file   [' + _author_attrib_fpath + ']\n')
            outfile.write(u'#\n')

            # print out pagerank sorted vector
            for i in self.__mapped_result_list :
                assert len(i) == 2
                outfile.write(i[0] + u'    ' + i[1] + u'\n')

            outfile.close()

        except IOError as e:
            print "Error! AuthorAttributeMapper.__save_result(): I/O error({0}): {1}".\
                  format(e.errno, e.strerror)
            sys.exit(1)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    def map_attribute(self, _author_vec_fpath, _author_attrib_fpath, _save_fpath):
        """map the author list to author attributes

        \parm[in] _author_vec_fpath     author vector file fullpath (UTF-8)
        \parm[in] _author_attrib_fpath  author attribute file fullpath (UTF-8)
        \parm[in] _save_fpath           save result file fullpath
        """
        ILog.info(u'author vector file    [' + _author_vec_fpath    + u']')
        ILog.info(u'author attribute file [' + _author_attrib_fpath + u']')
        ILog.info(u'output mapped file    [' + _save_fpath          + u']')

        self.__read_author_vector_file(_author_vec_fpath)
        self.__read_author_attribute_file(_author_attrib_fpath)

        # self.dump_author_attribute_list_map()

        self.__map_attribute()

        # print out reduced vector
        # for valid_author in self.__reduced_author_vec:
        #     print valid_author
        self.__save_result(_author_vec_fpath, _author_attrib_fpath, _save_fpath)


if __name__=="__main__":
    print u'# Usage: run the test_author_attrib_map_0.py.'
