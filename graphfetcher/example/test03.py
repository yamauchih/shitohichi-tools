#!/usr/bin/env python
#
# Copyright (C) 2012 Yamauchi, Hitoshi
#
# open the unicode filename and parse them
#

import os
import urllib
import urllib2
import BeautifulSoup

# to get the Nihon no shousetuka ichiran filename
def getRoot():
    mydatadir = '/home/hitoshi/data/project/shitohichi-tools/graphfetcher/ja.wikipedia.org/wiki/'
    for fn in os.listdir(mydatadir):
        # print fn
        url = 'file:///' + mydatadir + urllib.quote(fn)
        # data = urllib2.urlopen(url).read()
        # soup = BeautifulSoup.BeautifulSoup(data)
        # print soup.prettify()
        print 'parsed: ' + url
        # print 'parsed: ' + urllib.unquote(url)

# to list all the downloaded data
def main():
    mydatadir = '/home/hitoshi/data/project/shitohichi-tools/graphfetcher/data/ja.wikipedia.org/wiki/'
    for fn in os.listdir(mydatadir):
        # print fn
        url = 'file:///' + mydatadir + urllib.quote(fn)
        # data = urllib2.urlopen(url).read()
        # soup = BeautifulSoup.BeautifulSoup(data)
        # print soup.prettify()
        print 'parsed: ' + url
        # print 'parsed: ' + urllib.unquote(url)


if __name__=="__main__":
    main()
