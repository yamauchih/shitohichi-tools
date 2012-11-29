#!/bin/bash -x
# -*- coding: utf-8 -*-
#
# get German writers pages from Wikipedia ja. Average wait time is
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
wget --restrict-file-names=nocontrol --limit-rate=100K -e 'robots=off' --random-wait --wait=15 -r --level=1 -k -p http://ja.wikipedia.org/wiki/%E3%83%89%E3%82%A4%E3%83%84%E8%AA%9E%E4%BD%9C%E5%AE%B6%E3%81%AE%E4%B8%80%E8%A6%A7