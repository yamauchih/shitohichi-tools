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
import codecs
from bs4 import BeautifulSoup

class LinkVectorExtractorEnEn(object):
    """create a vector from a meta web page's link"""

    def __init__(self, _ignore_href_list):
        """constructor
        \param[in] _ignore_href_list ignore hyper link reference list
        """
        sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

        # this class of 'a' element has no link
        self.__ignore_link_class_set = {'new', 'noprint', 'image'}
        self.__ignore_href_substring_list = _ignore_href_list


    def can_add_entry(self, _link):
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
            if ( href_string.find(words) >= 0):
                return False
        return True


    def get_link_list(self, _root_url, _output_fname):
        """get link list
        \param[in] _root_url     root file URL
        \param[in] _output_fname output list filename
        """
        try:
            # open output file with utf-8 codec
            outfile = codecs.open(_output_fname, mode='w', encoding='utf-8')

            outfile.write(u'#LinkVectorExtractorEnEn 0\n');
            outfile.write(u'# generated by LinkVectorExtractorEnEn. (C) Hitoshi 2012\n');
            outfile.write(u'# input [' + _root_url     + ']\n');

            data = urllib2.urlopen(_root_url).read()
            soup = BeautifulSoup(data)
            linklist = soup.find_all('li')
            for link in linklist:
                atag = link.a
                if(atag == None):
                    # print 'Skip:', unicode(str(link), encoding='utf-8')
                    continue
                # print atag['href']
                # print unicode(str(atag['href']), encoding='utf-8', errors='replace')
                if self.can_add_entry(atag) == False:
                    # print 'ignore: ' + str(atag)
                    pass
                else:
                    # In Wiki, href and title are the same. No need to
                    # output both.
                    #
                    # outfile.write(link.get('href') + ' ' + link.get('title') + '\n');
                    outfile.write(atag.get('href') + '\n');

            outfile.close()
        except IOError as (errno, strerror):
            print "# I/O error({0}): {1}".format(errno, strerror)
            print '# Does output directory exist?'
            print '# Also you need LC_ALL setting to utf-8, e.g., en_US.utf-8, ja_JP.utf-8.'

        # Uncaught exception goes up.


if __name__=="__main__":

    print u'# Usage: run the test_linkvectorextractor_0.py.'
