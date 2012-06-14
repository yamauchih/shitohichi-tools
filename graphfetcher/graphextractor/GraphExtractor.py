#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Yamauchi, Hitoshi
# For Rebecca from Hitoshi the fool
#
# Graph extractor:
# Get a list of pair {URL, Val} and generate adjacent matrix between URLs.
#
# wget download web page has already been changed the url. I think all
# the pages are in one directory. (Assumption)
#

import os, sys
import urllib
import urllib2
import codecs
from bs4 import BeautifulSoup

class GraphExtractor(object):
    """Extract graph structure from a web pages.
    An adjacent matrix is generated."""

    def __init__(self, _test_url_list, _opt_dict):
        """constructor

        Options:

        - 'is_print_connectivity': bool. when True, print out the
          detected connectivity.

        - 'dot_file_name': string. When non empty, generate a dot file
          with this name. '' when not generate file.

        - 'is_generate_annotated_html': bool. when True, generate
          annotated html pages in the output directory. The connected
          link has a color.

        - 'is_remove_self_link': bool. when True, remove the self link.

        \param[in] _test_url_list if None, only analyze this list URL
        \param[in] _opt_dict options
        """
        sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

        # index to url map. list implementation
        self.__index_to_url_map = []
        # url to index map. dict implementation
        self.__url_to_index_map = {}

        # test URL list
        if _test_url_list == None:
            self.__test_url_list = []
        else:
            self.__test_url_list = _test_url_list

        # current working directory
        self.__cwd = u'./'

        # output directory
        self.__output_dir = u'./'

        # adjacent matrix: list of [index list], idx -> [index list]
        self.__M_ij = []

        # dot file name. if '', no dot file output
        self.__dot_file_name = u''
        self.__is_generate_dotfile = False
        # dot file ostream
        self.__dot_file_os = None

        #------------------------------------------------------------
        # options
        #------------------------------------------------------------
        # is_print_connectivity
        self.__is_print_connectivity = False;
        if (_opt_dict.has_key('is_print_connectivity')):
            self.__is_print_connectivity = _opt_dict['is_print_connectivity']
        print u'# Option: is_print_connectivity:', str(self.__is_print_connectivity)

        # dot file generation
        if (_opt_dict.has_key('dot_file_name')):
            self.__dot_file_name = _opt_dict['dot_file_name'].strip()
        if (len(self.__dot_file_name) > 0):
            self.__is_generate_dotfile = True
        print u'# Option: is_generate_dotfile:', str(self.__is_generate_dotfile),\
              u'[' + self.__dot_file_name + u']'

        # is_generate_annotated_html
        self.__is_generate_annotated_html = False;
        if (_opt_dict.has_key('is_generate_annotated_html')):
            self.__is_generate_annotated_html = _opt_dict['is_generate_annotated_html']
        print u'# Option: is_generate_annotated_html:', str(self.__is_generate_annotated_html)

        # is_remove_self_link
        self.__is_remove_self_link = False;
        if (_opt_dict.has_key('is_remove_self_link')):
            self.__is_remove_self_link = _opt_dict['is_remove_self_link']
        print u'# Option: is_remove_self_link:', str(self.__is_remove_self_link)


    def __load_input_vector(self, _input_vector_list_fname):
        """load input vector. The input file should be created by
        ListFetcher.  Store the input vector in a bijection map
        (a forward map and a backword map).

        \param[in] _input_vector_list_fname input vector list file name (current directory)
        """
        infile = codecs.open(_input_vector_list_fname, mode='r', encoding='utf-8')
        idx = 0
        for fline in infile:
            line = fline.strip()
            if ((len(line) > 0) and (line[0] != '#')):
                # non null and not started # line ... add to the map
                if (not self.__url_to_index_map.has_key(line)):
                    self.__url_to_index_map[line] = idx
                    self.__index_to_url_map.append(line)
                    idx = idx + 1
                else:
                    print u'duplication found [' + line + u'] at ' + str(idx) + \
                        u' ignored'

        assert len(self.__url_to_index_map) == len(self.__index_to_url_map)
        print '# number of entries: ', len(self.__index_to_url_map)

        # initialize adjacent matrix
        for i in xrange(0, len(self.__index_to_url_map)):
            self.__M_ij.append([])


    def __open_dot_file(self, _output_directory):
        """open dot file if needed. and outpout the header.
        \param[in] _output_directory output directory
        """
        if (self.__is_generate_dotfile != True):
            return

        out_full_path = os.path.join(_output_directory, self.__dot_file_name)
        self.__dot_file_os = codecs.open(out_full_path, mode='w', encoding='utf-8')

        # output header
        dotfile_header = u'// -*- encoding: utf-8 -*-\n' +\
                         u'//\n' +\
                         u'// dot file generated by GraphExtractor\n' +\
                         u'// Copyright (C) 2012 Yamauchi, Hitoshi\n' +\
                         u'// For Rebecca by Hitoshi the fool\n' +\
                         u'//\n' +\
                         u'// dot -Tsvg ' + self.__dot_file_name + ' -o ' +\
                         self.__dot_file_name + '.svg\n' +\
                         u'digraph Graph {\n'
        self.__dot_file_os.write(dotfile_header)


    def __output_node_to_dotfile(self, _node):
        """output a node with attribute into the dot file.
        \param[in] _node a node of the graph
        """
        assert self.__dot_file_os != None
        self.__dot_file_os.write(u'        ' + _node + u' [shape=plaintext, fontsize=7.0];\n')


    def __output_connectivity_to_dotfile(self, _from, _to):
        """output one connectivity to the dot file if it is opened.
        \param[in] _from connection from
        \param[in] _to   connection to
        """
        assert self.__dot_file_os != None
        self.__dot_file_os.write(u'        ' + _from + u' -> ' + _to + u';\n')


    def __close_dot_file(self):
        """close dot file if opened with outpout the footer.
        """
        if (self.__dot_file_os == None):
            assert self.__is_generate_dotfile == False
            return

        self.__dot_file_os.write(u'}\n')
        self.__dot_file_os.close()
        self.__dot_file_os = None


    def __append_annotation(self, _soup, _tag):
        """append annotation after _tag
        \param[in] _soup the soup
        \param[in] _tag  tag to be appended
        """
        append_tag = _soup.new_tag("font")
        append_tag.string = "(Connected)"
        append_tag['color'] = '#00ff00'
        _tag.insert_after(append_tag)


    def __export_current_soup(self, _soup, _fname):
        """export the current soup
        \param[in] _soup the beautiful soup object
        \param[in] _fname file name to output
        """
        out_full_path = os.path.join(self.__output_dir, _fname)
        print u'Writing [' + out_full_path + u']'
        if (os.path.isfile(out_full_path)):
            raise StandardError, ('Output file exists')

        outfile = codecs.open(out_full_path, mode='w', encoding='utf-8')
        outfile.write('<!-- connectivity annotated html generated by GraphExtractor by Hitoshi -->\n')
        outfile.write(unicode(_soup.prettify(formatter="html")) + '\n')


    def __get_one_page_connectivity(self, _url):
        """get one page connectivity
        \param[in] _url page URL
        """
        file_url = u'file://' + self.__cwd + _url
        # print file_url
        data = urllib2.urlopen(file_url).read()
        soup = BeautifulSoup(data)
        src_link_list = soup.find_all('a')
        dst_link_list = []

        # add node to the dotfile
        if (self.__is_generate_dotfile == True):
            self.__output_node_to_dotfile(_url)

        for link in src_link_list:
            dst = link.get('href')
            # If this (print dst) doesnot work, some file corruption
            # suspected. Sometimes see \E3 with gedit.
            # print dst
            if (self.__url_to_index_map.has_key(dst)):
                if (self.__is_remove_self_link):
                    if (_url == dst):
                        # print u'ignore self link [' + _url + u']->[' + dst + u']'
                        continue

                # Show connection
                if (self.__is_print_connectivity == True):
                    print u'connect [' + _url + u']->[' + dst + u']'

                # add connection to the dotfile
                if (self.__is_generate_dotfile == True):
                    self.__output_connectivity_to_dotfile(_url, dst)

                # add annotation (link)
                if (self.__is_generate_annotated_html == True):
                    self.__append_annotation(soup, link)

                # not yet duplication check
                # list(set(dst_link_list)) may remove duplication using set
                dst_link_list.append(self.__url_to_index_map[dst])


        # record the list
        idx = self.__url_to_index_map[_url]
        self.__M_ij[idx] = dst_link_list
        # FIXME: not exclude itself and duplicated links
        rec_links = len(dst_link_list)
        # print _url + u' has ' + str(rec_links) + u' recognizable links.'

        # export the document if is_generate_annotated_html is on
        if (self.__is_generate_annotated_html == True):
            self.__export_current_soup(soup, _url)

        return rec_links


    def __get_all_connectivity(self):
        """get all connectivity

        if self.__test_url_list has entries, use that entries for
        test, else analyze all url in the input vector.
        """
        if (len(self.__test_url_list) > 0):
            # test mode
            for url in self.__test_url_list:
                rec_link_count = self.__get_one_page_connectivity(url)
                print u'analyzed [' + url + u'] found ' + str(rec_link_count) +\
                    u' links.'
                if (rec_link_count == 0):
                    print u'Warning! ' + url + u' has no recognizable links. Check the URL input.'

        else:
            cur_i = 0
            total_len_str = str(len(self.__index_to_url_map))
            for url in self.__index_to_url_map:
                cur_i = cur_i + 1
                rec_link_count = self.__get_one_page_connectivity(url)
                print u'analyzed [' + url + u'] ' + str(cur_i) + u'/' + total_len_str +\
                    u' found ' + str(rec_link_count) + u' links.'
                if (rec_link_count == 0):
                    print u'Warning! ' + url + u' has no recognizable links. Check the URL input.'



    def __output_adjacent_matrix(self, _output_directory, _output_fname):
        """output adjacent matrix
        \param[in] _output_directory output directory
        \param[in] _output_fname output filename
        """
        outfname = os.path.join(_output_directory, _output_fname)
        outfile = codecs.open(outfname, mode='w', encoding='utf-8')
        outfile.write('# adjacent matrix generated by GraphExtractor by Hitoshi\n')
        outfile.write(str(self.__M_ij) + '\n')


    def get_adjacent_matrix(self,
                            _working_directory, _input_vector_list_fname,
                            _output_directory,  _output_Madj_fname):
        """get adjacent matrix
        \param[in] _working_directory working directory to cd, input html directory.
        \param[in] _input_vector_list_fname input vector list file name
        \param[in] _output_directory  output directory
        \param[in] _output_Madj_fname output adjacency matrix file name
        """
        os.chdir(_working_directory)
        self.__cwd = _working_directory
        self.__output_dir = _output_directory
        self.__load_input_vector(_input_vector_list_fname)
        self.__open_dot_file(_output_directory)
        self.__get_all_connectivity()
        self.__close_dot_file()
        self.__output_adjacent_matrix(_output_directory, _output_Madj_fname)


if __name__=="__main__":
    print 'Usage: test_graphextractor.py'
