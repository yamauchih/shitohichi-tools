#!/bin/bash -x
# -*- coding: utf-8 -*-
#
# get English writers from German Wikipedia. Average wait time is
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
# イギリスの小説家 Liste_britischer_Schriftsteller
# 英語の小説家     Liste_englischsprachiger_Schriftsteller
#
wget --restrict-file-names=nocontrol --limit-rate=100K -e 'robots=off' --random-wait --wait=15 -r --level=1 -k -p http://de.wikipedia.org/wiki/Liste_britischer_Schriftsteller

# wget --restrict-file-names=nocontrol --limit-rate=100K -e 'robots=off' --random-wait --wait=15 -r --level=1 -k -p http://de.wikipedia.org/wiki/Liste_englischsprachiger_Schriftsteller