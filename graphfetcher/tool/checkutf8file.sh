#!/bin/sh
#
# Check the utf-8 file is broken or not
# (C) 2012 Hitoshi Yamauchi
#
for i in $*
do
    echo $i
    iconv -f utf-8 -t utf-8 $i > /dev/null
done