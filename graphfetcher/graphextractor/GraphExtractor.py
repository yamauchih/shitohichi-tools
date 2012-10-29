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

import os, sys, urllib, urllib2, codecs
import SoupUtil
from bs4 import BeautifulSoup


class GraphExtractor(object):
    """Extract graph structure from a web pages.
    An adjacent matrix is generated."""

    def __init__(self, _test_url_list, _opt_dict):
        """constructor

        Options:

        - 'log_level': int. 0 ... error, 1 ... info, 2 ... debug level
          log output

        - 'is_print_connectivity': bool. when True, print out the
          detected connectivity.

        - 'is_enable_stdout_utf8_codec': bool. When True, sys.stdout is UTF8 outout
          when you see a conversion error, try set this.

        - 'dot_file_name': string. When non empty, generate a dot file
          with this name. '' when not generate file.

        - 'is_generate_annotated_html': bool. when True, generate
          annotated html pages in the output directory. The connected
          link has a color.

        - 'is_remove_self_link': bool. when True, remove the self link.

        - 'output_matrix_type': string. ['python', 'matlab']
           'python': python list
           'matlab': matlab sparse matrix

        - 'is_remove_navbox': bool (option) When True, <table class='navbox'></table>
           entries will be deleted. This is a special handling for the Japanese wiki.

        \param[in] _test_url_list if None, only analyze this list URL
        \param[in] _opt_dict options
        """
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
        self.__log_level = 2
        if (_opt_dict.has_key('log_level')):
            self.info_out(u'# Option: log_level: ' + str(_opt_dict['log_level']))
            self.__log_level = _opt_dict['log_level']
        else:
            self.info_out(u'# Option: log_level: ' + str(self.__log_level))


        # is_enable_stdout_utf8_codec
        if (_opt_dict.has_key('is_enable_stdout_utf8_codec')):
            if(_opt_dict['is_enable_stdout_utf8_codec'] == True):
                sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
                self.info_out(u'# Option: is_enable_stdout_utf8_codec: True')
            else:
                self.info_out(u'# Option: is_enable_stdout_utf8_codec: False')

        # is_print_connectivity
        self.__is_print_connectivity = False;
        if (_opt_dict.has_key('is_print_connectivity')):
            self.__is_print_connectivity = _opt_dict['is_print_connectivity']
        self.info_out(u'# Option: is_print_connectivity: ' + str(self.__is_print_connectivity))

        # dot file generation
        if (_opt_dict.has_key('dot_file_name')):
            self.__dot_file_name = _opt_dict['dot_file_name'].strip()
        if (len(self.__dot_file_name) > 0):
            self.__is_generate_dotfile = True
        self.info_out(u'# Option: is_generate_dotfile: ' + str(self.__is_generate_dotfile) +
                      u' [' + self.__dot_file_name + u']')

        # is_generate_annotated_html
        self.__is_generate_annotated_html = False;
        if (_opt_dict.has_key('is_generate_annotated_html')):
            self.__is_generate_annotated_html = _opt_dict['is_generate_annotated_html']
        self.info_out(u'# Option: is_generate_annotated_html: ' + str(self.__is_generate_annotated_html))

        # is_remove_self_link
        self.__is_remove_self_link = False;
        if (_opt_dict.has_key('is_remove_self_link')):
            self.__is_remove_self_link = _opt_dict['is_remove_self_link']
        self.info_out(u'# Option: is_remove_self_link:' + str(self.__is_remove_self_link))

        # output matrix type
        self.__output_matrix_type = 'python';
        if (_opt_dict.has_key('output_matrix_type')):
            self.__output_matrix_type = _opt_dict['output_matrix_type']
        valid_matrix_type_list = ['python', 'matlab']
        if (self.__output_matrix_type not in valid_matrix_type_list):
            raise StandardError, ('Unknown outout matrix type [' + self.__output_matrix_type + ']')
        self.info_out(u'# Option: output_matrix_type: ' + self.__output_matrix_type)

        # remove <table class='navbox'></table> entries?
        self.__is_remove_navbox = False
        if (_opt_dict.has_key('is_remove_navbox')):
            self.__is_remove_navbox = _opt_dict['is_remove_navbox']
            self.info_out(u'# Option: is_remove_navbox:' + str(self.__is_remove_navbox))


    def error_out(self, _mes):
        """errlr level log output"""
        if(self.__log_level == 0):
            print u'error:', _mes

    def info_out(self, _mes):
        """info level log output"""
        if(self.__log_level >= 1):
            print u'info:', _mes

    def debug_out(self, _mes):
        """debug level log output"""
        if(self.__log_level >= 2):
            print u'debug:', _mes


    def __load_input_vector(self, _input_vector_fpath):
        """load input vector. The input file should be created by
        ListFetcher.  Store the input vector in a bijection map
        (a forward map and a backword map).

        \param[in] _input_vector_fpath input vector list file name, fullpath
        """
        infile = codecs.open(_input_vector_fpath, mode='r', encoding='utf-8')
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
                    # duplication should not be allowed for graph extraction.
                    raise StandardError('Error: duplication found [' + str(line) + '] at ' + str(idx))


        assert len(self.__url_to_index_map) == len(self.__index_to_url_map)
        self.info_out('# number of entries: ' + str(len(self.__index_to_url_map)))

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
        self.info_out(u'Writing [' + out_full_path + u']')
        if (os.path.isfile(out_full_path)):
            raise StandardError, ('Output file exists')

        outfile = codecs.open(out_full_path, mode='w', encoding='utf-8')
        outfile.write('<!-- connectivity annotated html generated by GraphExtractor by Hitoshi -->\n')
        outfile.write(unicode(_soup.prettify(formatter="html")) + '\n')
        outfile.close()

    def __get_one_page_connectivity(self, _url):
        """get one page connectivity
        \param[in] _url page URL
        """
        file_url = u'file://' + self.__cwd + _url
        # print file_url
        data = urllib2.urlopen(file_url).read()
        soup = BeautifulSoup(data)

        # special handling for Japanese wiki: a bit of hack...
        if (self.__is_remove_navbox == True):
            SoupUtil.delete_navbox(soup)


        src_link_list = soup.find_all('a')
        dst_link_set = set()

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
                    self.info_out(u'connect [' + _url + u'](' + \
                                  str(self.__url_to_index_map[_url]) + ')->[' + \
                                  dst + u'](' + str(self.__url_to_index_map[dst]) +')')

                # add connection to the dotfile
                if (self.__is_generate_dotfile == True):
                    self.__output_connectivity_to_dotfile(_url, dst)

                # add annotation (link)
                if (self.__is_generate_annotated_html == True):
                    self.__append_annotation(soup, link)

                # if no duplication check, use list.
                #   dst_link_list.append(self.__url_to_index_map[dst])
                # if duplication check, use set.
                dst_link_set.add(self.__url_to_index_map[dst])

        # convert set to a list
        dst_link_list = list(dst_link_set)

        # record the list
        idx = self.__url_to_index_map[_url]
        self.__M_ij[idx] = dst_link_list
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
                self.debug_out(u'analyzed [' + url + u'] found ' + str(rec_link_count) +
                               u' links.')
                if (rec_link_count == 0):
                    self.debug_out(u'Warning! ' + url +
                                   u' has no recognizable links. Check the URL input.')

        else:
            cur_i = 0
            total_len_str = str(len(self.__index_to_url_map))
            for url in self.__index_to_url_map:
                cur_i = cur_i + 1
                rec_link_count = self.__get_one_page_connectivity(url)
                self.debug_out(u'analyzed [' + url + u'] ' + str(cur_i) + u'/' + total_len_str +
                               u' found ' + str(rec_link_count) + u' links.')
                if (rec_link_count == 0):
                    self.debug_out(u'Warning! ' + url +
                                   u' has no recognizable links. Check the URL input.')
                if ((cur_i % 100) == 0):
                    self.info_out('progress ' + str(cur_i) + u'/' + total_len_str)


    def __output_matlab_sparse_marix(self, _ostream, _output_fname):
        """output adjacent matrix in matlab sparse matrix format
        \param[in] _ostream output stream
        \param[in] _output_fname output m filename.
        The basename is the function name in M language.
        """
        n = len(self.__M_ij)
        base_ext_name = os.path.basename(_output_fname)
        (basename, ext) = os.path.splitext(base_ext_name)
        if (ext != '.m'):
            print u'warn: The output file name has no .m extension. Use function name as is [' +\
                  base_ext_name + u']'
            basename = base_ext_name

        matname = 'madj'
        _ostream.write('function [ {0} ] = {1}()\n'.format(matname, basename))
        _ostream.write('% adjacent {0}x{1} matrix generated by GraphExtractor\n'.
                       format(n, n))
        _ostream.write('% GraphExtractor (C) 2012 Hitoshi Yamauchi, Sunday Research\n')
        _ostream.write('% sparse(1:n, 1:n, 1) create sparse I\n')
        _ostream.write('{0} = sparse({1}, {2});\n'.format(matname, n, n))
        for r in xrange(0, n):
            rowlist = self.__M_ij[r]
            for c in rowlist:
                # matlab index starts with 1
                _ostream.write('{0}({1},{2}) = 1;\n'.format(matname, (r+1), (c+1)))


    def __output_adjacent_matrix(self, _output_directory, _output_fname):
        """output adjacent matrix
        \param[in] _output_directory output directory
        \param[in] _output_fname output filename, fullpath
        """
        outfile = codecs.open(_output_fname, mode='w', encoding='utf-8')

        if (self.__output_matrix_type == 'python'):
            outfile.write('# adjacent matrix generated by GraphExtractor by Hitoshi\n')
            outfile.write(str(self.__M_ij) + '\n')
        elif (self.__output_matrix_type == 'matlab'):
            self.__output_matlab_sparse_marix(outfile, _output_fname)
        else:
            raise StandardError, ('Unknown outout matrix type [' + self.__output_matrix_type + ']')

        outfile.close()


    def get_adjacent_matrix(self,
                            _working_directory, _input_vector_fpath,
                            _output_directory,  _output_madj_fpath):
        """get adjacent matrix
        \param[in] _working_directory working directory to cd, input html directory.
        \param[in] _input_vector_fpath input vector list file name, fullpath
        \param[in] _output_directory  output directory
        \param[in] _output_madj_fpath output adjacency matrix file name, fullpath
        """
        os.chdir(_working_directory)
        self.__cwd = _working_directory
        self.__output_dir = _output_directory
        self.__load_input_vector(_input_vector_fpath)
        self.__open_dot_file(_output_directory)
        self.__get_all_connectivity()
        self.__close_dot_file()
        self.__output_adjacent_matrix(_output_directory, _output_madj_fpath)


if __name__=="__main__":
    print 'Usage: test_graphextractor.py'
