#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Yamauchi, Hitoshi
# For Rebecca from Hitoshi the fool
#
# test pretty print by beautiful soup
#
"""
\file
\brief pretty print test by beautiful soup
"""

import os, sys, urllib, urllib2, codecs
from bs4 import BeautifulSoup

graphfetcherdir    = u'/home/hitoshi/data/project/shitohichi-tools/graphfetcher/'
input_rpath        = u'data/japanese_writer/ja.wikipedia.org/wiki/井上靖'

file_url = u'file://' + graphfetcherdir + input_rpath
# print file_url
data = urllib2.urlopen(file_url).read()
soup = BeautifulSoup(data)

#
# pretty print of html file
#
sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
print(soup.prettify())


#
# main test
#
if __name__ == '__main__':
    # suit0   = unittest.TestLoader().loadTestsFromTestCase(TestGraphExtractor)
    # alltest = unittest.TestSuite([suit0])
    # unittest.TextTestRunner(verbosity=2).run(alltest)
    pass

