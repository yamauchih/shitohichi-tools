#!/usr/bin/env python
#
# Copyright (C) 2012 Yamauchi, Hitoshi
#
#

import urllib2
import BeautifulSoup

def main():
    myprojdir = '/home/hitoshi/data/project/shitohichi-tools/graphfetcher/'
    url = 'file:///' + myprojdir + 'data/nihonnoshousetukaichiran_wiki.html'
    data = urllib2.urlopen(url).read()
    soup = BeautifulSoup.BeautifulSoup(data)

    print soup.prettify()


if __name__=="__main__":
    main()
