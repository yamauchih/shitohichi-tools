#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Yamauchi, Hitoshi
# For Rebecca from Hitoshi the fool
#
# test delete element (decompose() in beautiful soup)
#
"""
\file
\brief test delete element (decompose() in beautiful soup)
"""

import os, sys, urllib, urllib2, codecs
from bs4 import BeautifulSoup


def delete_navbox(_soup):
    """find the navbox (Award table in Japanese wiki) and delete it.

    \param[in] _soup beautiful soup instance
    """

    navbox_tb = _soup.find_all("table", { "class" : "navbox" })
    # print(navbox_tb)
    print 'navbox_tb len: ', len(navbox_tb)
    # navbox_tb[0]) is a tag

    #
    # remove the elements backward, since latter one can be a child. We
    # can not delete parents first, then children are also decomposed.
    #
    for i in range(len(navbox_tb) - 1, -1, -1):
        sys.stderr.write('decompose ' + str(i) + '\n')
        sys.stderr.write(str(navbox_tb[i].attrs) + '\n')
        navbox_tb[i].decompose()


def main():
    graphfetcherdir    = u'/home/hitoshi/data/project/shitohichi-tools/graphfetcher/'
    input_rpath        = u'data/japanese_writer/ja.wikipedia.org/wiki/井上靖'

    file_url = u'file://' + graphfetcherdir + input_rpath
    # print file_url
    data = urllib2.urlopen(file_url).read()
    soup = BeautifulSoup(data)

    delete_navbox(soup)

    sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
    print(soup.prettify())

#
# main test
#
if __name__ == '__main__':
    main()

