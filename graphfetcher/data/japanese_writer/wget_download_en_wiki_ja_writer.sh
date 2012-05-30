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
# The recursion level is 2, since the meta page only have each
# familyname meta page.
#
wget --restrict-file-names=nocontrol --limit-rate=100K -e 'robots=off' --random-wait --wait=15 -r --level=2 -k -p http://en.wikipedia.org/wiki/Japanese_writers
