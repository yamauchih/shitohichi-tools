#!/bin/bash -x
#
# get Japanese authors pages from Wikipedia ja. Average wait time is
# 15 seconds and limit rate 100k/sec max for not overloading the
# server.
#
# Hitoshi Yamauchi
#
# 2012-5-20(Sun)
#
wget --limit-rate=100K  --wait=15 -r --level=1 -k -p http://ja.wikipedia.org/wiki/%E6%97%A5%E6%9C%AC%E3%81%AE%E5%B0%8F%E8%AA%AC%E5%AE%B6%E4%B8%80%E8%A6%A7
