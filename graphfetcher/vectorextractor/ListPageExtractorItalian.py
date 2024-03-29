#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012-2013 Yamauchi, Hitoshi
# For Rebecca from Hitoshi the fool
#
# Open a unicode filename's html. Specialized for Italian meta page.
#

import os, sys, re, urllib, urllib2
import codecs, quopri
from bs4 import BeautifulSoup

class ListPageExtractorItalian(object):
    """create a vector from a meta web page's link"""

    def __init__(self, _ignore_href_list, _opt_dict):
        """constructor
        """
        # make stdout utf-8, some problem...
        #sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
        #sys.stderr = codecs.getwriter('utf_8')(sys.stderr)

        # this class of 'a' element has no link
        # self.__ignore_link_class_set = {'new', 'noprint', 'image'}
        # self.__ignore_href_substring_list = _ignore_href_list
        # self.__opt_dict   = _opt_dict
        # self.__entry_list = []
        # self.__entry_set  = set()        # for duplication check
        # self.__read_file  = []           # record read files
        # # print _opt_dict
        self.__tag_in_each_link = _opt_dict['tag_in_each_link']
        assert(self.__tag_in_each_link != None)
        # self.__blacklist_set = None
        # if('blacklistset' in _opt_dict):
        #     self.__blacklist_set = _opt_dict['blacklistset']


        self.__exclude_name_list = [
            'Aiuto:',
            'Portale:',
            'Speciale:',
            'Wikipedia:'
            ]

        self.__added_entry = set()

        # don't add the root node.
        self.__added_entry.add('Categoria:Scrittori_italiani')



    # def __print_str(self, _str):
    #     """convenient function for print unicode or string using utf-8
    #     without casting exception.
    #     \param[in] _str type unicode or type str.
    #     """
    #     if type(_str) == type(u'a'):
    #         sys.stdout.write(_str.encode('utf-8', 'replace') + '\n')
    #     else:
    #         sys.stdout.write(_str + '\n')

    def __can_add_entry_by_name(self, _wiki_entry):
        """check the _wiki_entry name which can add.
        For instance 'Speciale:*' or 'Wikipedia:*' is neither the
        author or author category. So We don't add them.
        """
        for ename in self.__exclude_name_list:
            if(_wiki_entry.find(ename) >= 0):
                return False
        return True


    def __can_add_entry(self, _wiki_entry):
        """check the _wiki_entry can be add
        \param[in] _wiki_entry
        \return True when you can add to the list
        """

        # check the name can be add
        if(self.__can_add_entry_by_name(_wiki_entry) == False):
            return False

        # don't add twice
        if (_wiki_entry in self.__added_entry):
            return False

        return True

    def get_link_list(self, _root_url):
        """get link list
        \param[in] _root_url     root file URL
        """
        try:
            data = urllib2.urlopen(_root_url).read()
            soup = BeautifulSoup(data)
            linklist = soup.find_all(self.__tag_in_each_link)
            for link in linklist:
                atag = link.a
                if(atag == None):
                    # print 'Skip:', unicode(str(link), encoding='utf-8')
                    continue
                href_item = atag.get('href')
                if (href_item != None):
                    href_unquote_item = urllib.unquote(href_item)
                    # filter it.wikipedia.org
                    re_it_wiki = re.compile(u"http://it.wikipedia.org/wiki/")
                    if (re_it_wiki.search(href_unquote_item) != None):
                        wiki_entry = re_it_wiki.sub('', href_unquote_item)
                        if(self.__can_add_entry(wiki_entry) == True):
                            sys.stdout.write(wiki_entry + '\n')
                        # else:
                        #     sys.stdout.write('Not added: ' + wiki_entry + '\n')

                        # HEREHERE

            # record read file
            # self.__read_file.append(_root_url)

        except IOError as (errno, strerror):
            print "# I/O error({0}): {1}".format(errno, strerror)
            print '# Also you need LC_ALL setting to utf-8, e.g., en_US.utf-8, ja_JP.utf-8.'

        # Uncaught exception goes up.


    # def export_to_file(self, _output_fname):
    #     """export entry list to a file.
    #     \param[in] _output_fname output filename
    #     """
    #     try:
    #         if len(self.__read_file) == 0:
    #             raise StandardError('No file has been read.')

    #         # open output file with utf-8 codec
    #         outfile = codecs.open(_output_fname, mode='w', encoding='utf-8')

    #         outfile.write(u'#AuthorVector 0\n');
    #         outfile.write(u'# generated by ListPageExtractorItalian. (C) Hitoshi\n');
    #         outfile.write(u'# number of input files ' + str(len(self.__read_file)) + '\n');
    #         for f in self.__read_file:
    #             outfile.write(u'# input [' + f + ']\n');
    #         outfile.write(u'# item size: ' + str(len(self.__entry_list)) + '\n');

    #         export_encoding = 'utf-8'
    #         if ('export_encoding' in self.__opt_dict):
    #             export_encoding = self.__opt_dict['export_encoding']
    #         outfile.write(u'# export encoding: ' + export_encoding + '\n');

    #         # if optional result_path_split exists, filter
    #         if('result_path_split' in self.__opt_dict):
    #             if(self.__opt_dict['result_path_split'] == True):
    #                 for i in xrange(0, len(self.__entry_list)):
    #                     (dir, fname) = os.path.split(self.__entry_list[i])
    #                     self.__entry_list[i] = fname

    #         if (export_encoding != 'utf-8'):
    #             for i in self.__entry_list:
    #                 outfile.write(i.encode(export_encoding, 'replace') + '\n');
    #         else:
    #             for i in self.__entry_list:
    #                 outfile.write(i + '\n');


    #         outfile.close()

    #     except IOError as (errno, strerror):
    #         print "# I/O error({0}): {1}".format(errno, strerror)
    #         print '# Does output directory exist?'
    #         print '# Also you need LC_ALL setting to utf-8, e.g., en_US.utf-8, ja_JP.utf-8.'


if __name__=="__main__":

    print u'# Usage: run the test_linkvectorextractor_en_en_0.py.'
