#!/bin/bash -x
# -*- coding: utf-8 -*-
#
# get Japanese writers from Wikipedia en. Average wait time is
# 15 seconds and limit rate 100k/sec max for not overloading the
# server.
#
# Hitoshi Yamauchi
#
# 2012-5-29(Tue)
#
# when --restrict-file-names=unix (default), some of the UTF-8
# characters are escaped with %hex values. So I need to set nocontrol
# and export LC_ALL=en_US.utf-8 to see the files.
#
# I first set recursion level 2, but then so many unrelated pages are
# downloaded, therefore I specify all the list pages.
#
wget --restrict-file-names=nocontrol --limit-rate=100K -e 'robots=off' --random-wait --wait=15 -r --level=1 -k -p \
    http://en.wikipedia.org/wiki/List_of_Japanese_authors:A	\
    http://en.wikipedia.org/wiki/List_of_Japanese_authors:B	\
    http://en.wikipedia.org/wiki/List_of_Japanese_authors:C	\
    http://en.wikipedia.org/wiki/List_of_Japanese_authors:D	\
    http://en.wikipedia.org/wiki/List_of_Japanese_authors:E	\
    http://en.wikipedia.org/wiki/List_of_Japanese_authors:F	\
    http://en.wikipedia.org/wiki/List_of_Japanese_authors:G	\
    http://en.wikipedia.org/wiki/List_of_Japanese_authors:H	\
    http://en.wikipedia.org/wiki/List_of_Japanese_authors:I	\
    http://en.wikipedia.org/wiki/List_of_Japanese_authors:J	\
    http://en.wikipedia.org/wiki/List_of_Japanese_authors:K	\
    http://en.wikipedia.org/wiki/List_of_Japanese_authors:L	\
    http://en.wikipedia.org/wiki/List_of_Japanese_authors:M	\
    http://en.wikipedia.org/wiki/List_of_Japanese_authors:N	\
    http://en.wikipedia.org/wiki/List_of_Japanese_authors:O	\
    http://en.wikipedia.org/wiki/List_of_Japanese_authors:P	\
    http://en.wikipedia.org/wiki/List_of_Japanese_authors:Q	\
    http://en.wikipedia.org/wiki/List_of_Japanese_authors:R	\
    http://en.wikipedia.org/wiki/List_of_Japanese_authors:S	\
    http://en.wikipedia.org/wiki/List_of_Japanese_authors:T	\
    http://en.wikipedia.org/wiki/List_of_Japanese_authors:U	\
    http://en.wikipedia.org/wiki/List_of_Japanese_authors:V	\
    http://en.wikipedia.org/wiki/List_of_Japanese_authors:W	\
    http://en.wikipedia.org/wiki/List_of_Japanese_authors:X	\
    http://en.wikipedia.org/wiki/List_of_Japanese_authors:Y	\
    http://en.wikipedia.org/wiki/List_of_Japanese_authors:Z
