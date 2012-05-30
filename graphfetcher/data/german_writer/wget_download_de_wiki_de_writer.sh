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
# German metapage also has only the Familyname list, so the recursion
# level is 2 here.
#
#
wget --restrict-file-names=nocontrol --limit-rate=100K -e 'robots=off' --random-wait --wait=15 -r --level=2 -k -p http://de.wikipedia.org/wiki/Liste_deutschsprachiger_Schriftsteller
