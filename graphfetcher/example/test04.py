#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Yamauchi, Hitoshi
#
# open the unicode filename and parse them
#

import os, sys
import urllib
import urllib2
import codecs
from bs4 import BeautifulSoup

def main():
    sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

    mydatadir = '/home/hitoshi/data/project/shitohichi-tools/graphfetcher/data/ja.wikipedia.org/wiki/'
    # This doesn't work
    # %E6%97%A5%E6%9C%AC%E3%81%AE%E5%B0%8F%E8%AA%AC%E5%AE%B6%E4%B8%80%E8%A6%A7
    # The following is obtained by test03.py
    # authorRootFilename = '%E6%2597%A5%E6%259C%AC%E3%2581%AE%E5%B0%258F%E8%AA%AC%E5%AE%B6%E4%B8%2580%E8%A6%A7'
    authorRootFilename = urllib.quote('日本の小説家一覧')

    url = 'file:///' + mydatadir + authorRootFilename
    print 'parsed: ' + url
    data = urllib2.urlopen(url).read()
    soup = BeautifulSoup(data)
    print soup.prettify()



if __name__=="__main__":
    main()
