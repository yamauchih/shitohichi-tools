#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Yamauchi, Hitoshi
# For Rebecca from Hitoshi the fool
#
# Open a unicode filename's html and get the list of 'li' elements and
# get the first a element. Optimized for english authors of Wikipedia en.
#

import os, sys
import urllib
import urllib2
import codecs, quopri
from bs4 import BeautifulSoup

class LinkVectorExtractor(object):
    """create a vector from a meta web page's link"""

    def __init__(self, _ignore_href_list, _optdict):
        """constructor
        \param[in] _ignore_href_list    ignore hyper link reference list
        \param[in] _optdict     option dict
                    - 'export_encoding': ['utf-8'|'ascii'|'shift_jis']
        """
        # make stdout utf-8, some problem...
        #sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
        #sys.stderr = codecs.getwriter('utf_8')(sys.stderr)

        # this class of 'a' element has no link
        self.__ignore_link_class_set = {'new', 'noprint', 'image'}
        self.__ignore_href_substring_list = _ignore_href_list
        self.__optdict = _optdict
        self.__entry_list = []
        self.__entry_set = set()        # for duplication check
        self.__read_file = []           # record read files
        # print _optdict
        self.__tag_in_each_link = _optdict['tag_in_each_link']
        assert(self.__tag_in_each_link != None)

    def __print_str(self, _str):
        """convenient function for print unicode or string using utf-8
        without casting exception.
        \param[in] _str type unicode or type str.
        """
        if type(_str) == type(u'a'):
            sys.stdout.write(_str.encode('utf-8', 'replace') + '\n')
        else:
            sys.stdout.write(_str + '\n')


    def __can_add_entry(self, _link):
        """check the _link has real link in Wiki
        \param[in] _link a link entry, i.e. 'a' entry
        \return True when a link exists
        """
        # filter out a specific class
        linkclass = _link.get('class')
        if ((linkclass != None) and (len(linkclass) > 0) and \
                (linkclass[0] in self.__ignore_link_class_set)):
            return False

        # no title means no link
        linktitle = _link.get('title')
        if (linktitle == None):
            return False

        # filter out some specific links in Wikipedia
        href_string = _link.get('href')
        for words in self.__ignore_href_substring_list:
            if (href_string.find(words) >= 0):
                return False

        return True

    def __is_duplicated(self, _entry_set, _href_item):
        """check the item duplication
        \param[in] _entry_set entry set they have already submitted.
        \param[in] _href_item the item to be checked duplication
        \return True when duplication found
        """
        if (_href_item in _entry_set):
            return True
        return False


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
                # print atag['href']
                # print unicode(str(atag['href']), encoding='utf-8', errors='replace')
                if (self.__can_add_entry(atag) == False):
                    # print 'ignore: ' + str(atag)
                    pass
                else:
                    href_item = atag.get('href')
                    # check duplication
                    if (self.__is_duplicated(self.__entry_set, href_item) == False):
                        # Adding to the output entry list
                        self.__entry_list.append(href_item)
                        self.__entry_set.add(href_item)
                    else:
                        dupstr = u'info: found duplication [{0}]'.format(href_item)
                        self.__print_str(dupstr)

            # record read file
            self.__read_file.append(_root_url)

        except IOError as (errno, strerror):
            print "# I/O error({0}): {1}".format(errno, strerror)
            print '# Also you need LC_ALL setting to utf-8, e.g., en_US.utf-8, ja_JP.utf-8.'

        # Uncaught exception goes up.


    def export_to_file(self, _output_fname):
        """export entry list to a file.
        \param[in] _output_fname output filename
        """
        try:
            if len(self.__read_file) == 0:
                raise StandardError('No file has been read.')

            # open output file with utf-8 codec
            outfile = codecs.open(_output_fname, mode='w', encoding='utf-8')

            outfile.write(u'#LinkVectorExtractor 0\n');
            outfile.write(u'# generated by LinkVectorExtractor. (C) Hitoshi 2012\n');
            outfile.write(u'# number of input files ' + str(len(self.__read_file)) + '\n');
            for f in self.__read_file:
                outfile.write(u'# input [' + f + ']\n');
            outfile.write(u'# item size: ' + str(len(self.__entry_list)) + '\n');

            export_encoding = 'utf-8'
            if ('export_encoding' in self.__optdict):
                export_encoding = self.__optdict['export_encoding']
            outfile.write(u'# export encoding: ' + export_encoding + '\n');

            if (export_encoding != 'utf-8'):
                for i in self.__entry_list:
                    outfile.write(i.encode(export_encoding, 'replace') + '\n');
            else:
                for i in self.__entry_list:
                    outfile.write(i + '\n');


            outfile.close()

        except IOError as (errno, strerror):
            print "# I/O error({0}): {1}".format(errno, strerror)
            print '# Does output directory exist?'
            print '# Also you need LC_ALL setting to utf-8, e.g., en_US.utf-8, ja_JP.utf-8.'


if __name__=="__main__":

    print u'# Usage: run the test_linkvectorextractor_en_en_0.py.'
