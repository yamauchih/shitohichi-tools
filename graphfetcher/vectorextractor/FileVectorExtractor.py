#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Yamauchi, Hitoshi
# For Rebecca from Hitoshi the fool
#
# Scan directory and generate the vector. Use blacklist.
#

import os, sys, re, math
import urllib
import urllib2
import codecs
from bs4 import BeautifulSoup

class FileVectorExtractor(object):
    """create a vector from scanning a directory with a blacklist.
    Then check the file and get the category, if category has a writer
    entry, the file is most likely a writer.
    """

    def __init__(self):
        """constructor
        """
        sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
        # black list. If there is an entry here, not considered as an author
        self.__black_list_set = set()
        # result author list
        self.__author_list = []
        self.__author_regex = \
            re.compile('writer|author|novelist|poets|dramatists|playwrights', re.IGNORECASE)
        self.__is_show_proegress = True


    def __show_progress(self, _cur_file_idx, _file_count):
        """show progress if self.__is_show_proegress True.
        \param[in] _cur_file_idx current processing file index
        \param[in] _file_count   number of total files
        """
        if (self.__is_show_proegress == False):
            return

        if(_file_count == 0):
            raise StandardError('no file found.')

        # show progress for each 5% (20 steps)
        digit = math.modf(math.log10(_file_count))[1]
        if(digit < 3):
            print "prog: [{0}%] {1}/{2}".format((100 * _cur_file_idx) /_file_count,
                                                _cur_file_idx, _file_count)
        else:
            digit = digit - 2
            skipstep10 = math.pow(10, digit)
            if ((_cur_file_idx % skipstep10) == 0):
                print "prog: [{0}%] {1}/{2}".format((100 * _cur_file_idx) /_file_count,
                                                    _cur_file_idx, _file_count)


    def read_blacklist(self, _blacklist_fname):
        """read blacklist file and keep in the set.
        \param[in] _blacklist_fname blacklist filename"""
        try:
            blacklist_f = codecs.open(_blacklist_fname, mode='r', encoding='utf-8')
            line_idx = 0
            for fline in blacklist_f:
                line_idx = line_idx + 1
                line = fline.strip()
                if ((len(line) > 0) and (line[0] != '#')):
                    # non null and not started # line ... add to the set
                    if (line in self.__black_list_set):
                        print u'duplication found [' + line + u'] at ' + str(line_idx) + \
                            u' ignored'
                    else:
                        self.__black_list_set.add(line)

            print u'read blacklist_file [' + _blacklist_fname + \
                u'], number of entries: ' + str(len(self.__black_list_set))
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            print "Can not open a blacklist file {0}".format(_blacklist_fname)
            print "Please create blacklist file (an empty file is also fine.)"
            sys.exit(1)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise


    def has_writer_description(self, _fname):
        """check _fname has writer description
        """
        # print u'info: checking ['+ _fname + u']'

        #
        # It seems some filename is not considered unicode (even I
        # made a unicode string with u'', so make sure the encoding is
        # utf-8. For example, Lemprière's_Bibliotheca_Classica can not
        # be passed in urlopen. 2012-7-29(Sun) Hitoshi
        #
        data = urllib2.urlopen(_fname.encode('utf-8')).read()
        soup = BeautifulSoup(data)

        # check persondata table
        persondata_tab = soup.find_all('table', { "id" : "persondata" })
        if (persondata_tab != None):
            for pd in persondata_tab:
                # pd.text
                mat = self.__author_regex.search(pd.text)
                if(mat != None):
                    #print u'debug: found in persondata: ' + mat.string[mat.start():mat.end()]
                    return True

        # check category link
        catlinks = soup.find_all('div', { "id" : "mw-normal-catlinks" })
        if ((catlinks != None) and (len(catlinks) > 0)):
            for cat in catlinks[0].find_all('a'):
                # print cat.text
                mat = self.__author_regex.search(cat.text)
                if(mat != None):
                    # print u'debug: found in category: ' + mat.string[mat.start():mat.end()]
                    return True

        return False


    def get_vector(self, _input_dir, _output_file):
        """get vector from scanning directory.
        \param[in] _input_dir    input files' directory
        \param[in] _output_file  output file name
        """
        if (not os.path.exists(_input_dir)):
            raise StandardError, ('No such input directory [' + _input_dir + ']')
        if (os.path.exists(_output_file)):
            raise StandardError, ('Output file exists [' + _output_file + ']')

        try:
            outfile = codecs.open(_output_file, mode='w', encoding='utf-8')
            outfile.write(u'#FileVectorExtractor 0\n');
            outfile.write(u'# generated by FileVectorExtractor. (C) Hitoshi 2012\n');
            outfile.write(u'# input directory [' + _input_dir + ']\n');

            os.chdir(_input_dir)
            flist = os.listdir(".")
            file_count = len(flist)
            cur_file_idx = 0
            flist.sort()
            for fname in flist:
                if (not os.path.isfile(fname)):
                    continue

                cur_file_idx = cur_file_idx + 1
                self.__show_progress(cur_file_idx, file_count)

                ufname = unicode(fname, encoding='utf-8', errors='strict')

                # if (ufname != u"Lemprière's_Bibliotheca_Classica"): # DEBUG
                #     continue

                if (ufname in self.__black_list_set):
                    print ufname, 'is in the blacklist. continue.'
                    continue                # in the blacklist

                url = u'file:///' + os.path.join(_input_dir, ufname)

                if (self.has_writer_description(url)):
                    self.__author_list.append(ufname)
                    # print u'found author [' + ufname + ']'
                else:
                    print u'info: seems not an author [' + ufname + ']'

            # output
            for auth in self.__author_list:
                outfile.write(auth + u'\n');

        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            print "Can not open a output file {0}".format(_output_file)
            sys.exit(1)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise


if __name__=="__main__":

    print u'# Usage: run the test_filevectorextractor_0.py.'
