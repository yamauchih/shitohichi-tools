#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Yamauchi, Hitoshi
#
# Open a unicode filename's html and get the list of 'a' elements.
# Optimized for Wikipedia ja
#

import os, sys
import urllib
import urllib2
import codecs
from bs4 import BeautifulSoup


class ListFetcher(object):
    """create link list from a meta page"""

    def __init__(self):
        """constructor
        """
        sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

        # this class of 'a' element has no link
        self.__ignore_link_class_set = {'new', 'noprint', 'image'}
        self.__ignore_href_substring_list = [
            '../w/index.php', 'Category', '/wiki', 'Wikipedia:', 'Portal', u'特別',
            'Help', 'http://wikimediafoundation.org', u'小説', u'作家', u'一覧',
            u'日本', u'メインページ', u'協定世界時' ]


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


    def get_link_list(self, _root_url):
        """get link list
        \param[in] _root_url
        """
        data = urllib2.urlopen(_root_url).read()
        soup = BeautifulSoup(data)
        linklist = soup.find_all('a')
        for link in linklist:
            # print link.get('class')
            if self.can_add_entry(link) == False:
                # print 'ignore: ' + str(link)
                pass
            else:
                print link.get('href')

        # sys.stdout.write(unicode(linklist))
        # print linklist



if __name__=="__main__":
    mydatadir = '/home/hitoshi/data/project/shitohichi-tools/graphfetcher/data/ja.wikipedia.org/wiki/'
    authorRootFilename = u'日本の小説家一覧'
    root_url = 'file:///' + mydatadir + authorRootFilename
    lf = ListFetcher()
    lf.get_link_list(root_url)
