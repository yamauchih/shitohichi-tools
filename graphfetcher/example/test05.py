#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Yamauchi, Hitoshi
#
# Modifying the element
#

import os, sys
import urllib
import urllib2
import codecs
from bs4 import BeautifulSoup

def main():
    sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

    markup = '<a href="MishimaYukio" title="Mishima Yukio">Mishima Yukio</a>\n' +\
        '<a href="NatumeSouseki" title="Natume Souseki">Natume Souseki</a>\n'

    soup = BeautifulSoup(markup)
    src_link_list = soup.find_all('a')
    for link in src_link_list:
        tag = soup.new_tag("font")
        tag.string = "(Connected)"
        tag['color'] = '#00ff00'
        link.insert_after(tag)

    print(soup.prettify(formatter='html'))


if __name__=="__main__":
    main()

