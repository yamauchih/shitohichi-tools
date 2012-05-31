#!/bin/bash -x
# -*- coding: utf-8 -*-
#
# get German writers pages from Wikipedia de. Average wait time is
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
# downloaded, therefore I specify all the list pages. There is no X
# and Y pages.
#
#
wget --restrict-file-names=nocontrol --limit-rate=100K -e 'robots=off' --random-wait --wait=15 -r --level=1 -k -p \
    http://de.wikipedia.org/wiki/Liste_deutschsprachiger_Schriftsteller/A	\
    http://de.wikipedia.org/wiki/Liste_deutschsprachiger_Schriftsteller/B	\
    http://de.wikipedia.org/wiki/Liste_deutschsprachiger_Schriftsteller/C	\
    http://de.wikipedia.org/wiki/Liste_deutschsprachiger_Schriftsteller/D	\
    http://de.wikipedia.org/wiki/Liste_deutschsprachiger_Schriftsteller/E	\
    http://de.wikipedia.org/wiki/Liste_deutschsprachiger_Schriftsteller/F	\
    http://de.wikipedia.org/wiki/Liste_deutschsprachiger_Schriftsteller/G	\
    http://de.wikipedia.org/wiki/Liste_deutschsprachiger_Schriftsteller/H	\
    http://de.wikipedia.org/wiki/Liste_deutschsprachiger_Schriftsteller/I	\
    http://de.wikipedia.org/wiki/Liste_deutschsprachiger_Schriftsteller/J	\
    http://de.wikipedia.org/wiki/Liste_deutschsprachiger_Schriftsteller/K	\
    http://de.wikipedia.org/wiki/Liste_deutschsprachiger_Schriftsteller/L	\
    http://de.wikipedia.org/wiki/Liste_deutschsprachiger_Schriftsteller/M	\
    http://de.wikipedia.org/wiki/Liste_deutschsprachiger_Schriftsteller/N	\
    http://de.wikipedia.org/wiki/Liste_deutschsprachiger_Schriftsteller/O	\
    http://de.wikipedia.org/wiki/Liste_deutschsprachiger_Schriftsteller/P	\
    http://de.wikipedia.org/wiki/Liste_deutschsprachiger_Schriftsteller/Q	\
    http://de.wikipedia.org/wiki/Liste_deutschsprachiger_Schriftsteller/R	\
    http://de.wikipedia.org/wiki/Liste_deutschsprachiger_Schriftsteller/S	\
    http://de.wikipedia.org/wiki/Liste_deutschsprachiger_Schriftsteller/T	\
    http://de.wikipedia.org/wiki/Liste_deutschsprachiger_Schriftsteller/U	\
    http://de.wikipedia.org/wiki/Liste_deutschsprachiger_Schriftsteller/V	\
    http://de.wikipedia.org/wiki/Liste_deutschsprachiger_Schriftsteller/W	\
    http://de.wikipedia.org/wiki/Liste_deutschsprachiger_Schriftsteller/Z
