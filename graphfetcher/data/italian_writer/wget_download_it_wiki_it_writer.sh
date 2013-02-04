#!/bin/bash -x
# -*- coding: utf-8 -*-
#
# get Italian writers from English Wikipedia. Average wait time is
# 15 seconds and limit rate 100k/sec max for not overloading the
# server.
#
# Hitoshi Yamauchi
#
# 2013-1-23(Wed)
#
# when --restrict-file-names=unix (default), some of the UTF-8
# characters are escaped with %hex values. So I need to set nocontrol
# and export LC_ALL=en_US.utf-8 to see the files.
#
wget --restrict-file-names=nocontrol --limit-rate=100K -e 'robots=off' --random-wait --wait=15 -r --level=2 -k -p http://it.wikipedia.org/wiki/Categoria:Scrittori_italiani
