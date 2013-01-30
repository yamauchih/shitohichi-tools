#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012-2013 Yamauchi, Hitoshi
# For Rebecca from Hitoshi the fool
#
# function argument behavior test.
#

def func(alist):
    listlen = len(alist)
    if (listlen < 3):
        raise StandardError('list length is too short.')

    # alist is passed by a kind of reference
    # The ocntents can be changed.
    alist[0] = 8

    # this makes alist copy (alist[:] is total copy)
    alist = alist[2:listlen-1]
    print 'in func 1: ', str(alist)

    # copied object is changed, but this change can not be seen from the main.
    alist[0] = 100
    print 'in func 2: ', str(alist)


if __name__=="__main__":
    alist = [1,2,3,4,5,6]
    func(alist)
    print 'in main:   ', str(alist)
