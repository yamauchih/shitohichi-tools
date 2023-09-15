#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# 2023 (C) Hitoshi Yamauchi
# Wordpress qTranslator clean up script
#
# New BSD License
#

import os, sys, argparse
import re

class Remove_qtrans(object):
    """Wordpress qTranslator clean up script
    Remove one language
    """

    def __init__(self, opt_dict):
        """constructor

        \param[in] opt_dict options
        """
        # index to url map. list implementation
        self.__opt_dict     = opt_dict
        self.__is_verbose   = opt_dict['verbose']
        self.__cur_lang     = opt_dict['language']
        self.verbose(f"Current lang: {self.__cur_lang}")

        # set up lang marker
        self.__cur_lang_marker = f"[:{opt_dict['language']}]"
        self.__re_other_lang_marker = re.compile(r"\[:\w\w\]|\[:\]")
        self.__re_split_token = re.compile(r"(\[:ja\]|\[:en\]|\[:de\]|\[:\])")

        # Is the current line is inside the __cur_lang?
        self.__inside_rm = False

        # result txt line lists
        self.__pass_line_list   = []
        self.__remove_line_list = []


    def verbose(self, mes):
        if (self.__is_verbose):
            print(f"# verbose: {mes}")

    def __process_line(self, line, line_number):
        """
        Assume the lang marker does not show twice in a line
        param[in] line        current processing line
        param[in] line_number current processing line number
        """
        token_list = self.__re_split_token.split(line)
        pass_list = []
        remove_list = []

        if (self.__inside_rm == True):
            # inside rm process
            for token in token_list:
                if (token == self.__cur_lang_marker):
                    # Note: Do not consider the new current marker starts in the same line.
                    raise RuntimeError(f"double language marker {self.__cur_lang_marker} at line: {line_number}")
                elif (self.__inside_rm and (self.__re_other_lang_marker.match(token) != None)):
                    # found end marker
                    self.verbose(f"multiline end marker {self.__re_other_lang_marker.match(token).group(0)} found at line: {line_number}")
                    self.__inside_rm = False
                    # case: end marker is [:] instead of other lang
                    if (token == "[:]"):
                        remove_list.append(token)
                    else:
                        # add the token to pass
                        pass_list.append(token)
                elif (self.__inside_rm == False):
                    # this line found the end marker
                    pass_list.append(token)
                else:
                    remove_list.append(token)

            # print(f"# multi rm:    {''.join(remove_list)}")
            # print(f"# multi pass:  {''.join(pass_list)}")

        else:
            # still outside
            in_line_in = False
            for token in token_list:
                if (token == self.__cur_lang_marker):
                    # found cur lang
                    self.verbose(f"match start {self.__cur_lang_marker} at line: {line_number}")
                    in_line_in = True
                    remove_list.append(token)
                elif (in_line_in and (self.__re_other_lang_marker.match(token) != None)):
                    ma = self.__re_other_lang_marker.match(token)
                    self.verbose(f"match end   not {self.__cur_lang_marker} but {ma.group(0)} at line: {line_number}")
                    in_line_in = False
                    if (token == "[:]"):
                        remove_list.append(token)
                    else:
                        # add the token to pass
                        pass_list.append(token)
                    remove_list.append('\n') # for pretty print of removed text
                else:
                    if (in_line_in == True):
                        remove_list.append(token)
                    else:
                        pass_list.append(token)

            if (in_line_in == True):
                # still inside
                self.__inside_rm = True
                self.verbose(f"multiline inside found at line: {line_number}")

            # print(f"# in-out rm:   {''.join(remove_list)}")
            # print(f"# in-out pass: {''.join(pass_list)}")

        self.__pass_line_list.  append(''.join(pass_list))
        self.__remove_line_list.append(''.join(remove_list))



    def run(self):
        """
        run the remove language
        """
        infname = self.__opt_dict["infile"]

        # [:ja]日本語[:en]English[:de]Deutsch[:]  en
        # [:ja]日本語[:de]Deutsch[:]
        # [:ja]日本語[:]
        # \\[:ja\\].*\\(\\[:en\\]\\|\\[:de\\]\\|\\[:\\]\\)

        with open(infname, mode='r') as xmlfile:
            fdata = xmlfile.readlines()
            line_number = 0
            for line in fdata:
                line_number += 1
                self.__process_line(line, line_number)

        with open(self.__opt_dict["outfile"], mode='w') as outfile:
            for line in self.__pass_line_list:
                if (line != ''):
                    outfile.write(line)
            self.verbose(f"output file: {self.__opt_dict['outfile']}")

        with open(self.__opt_dict["rmfile"], mode='w') as rmfile:
            for line in self.__remove_line_list:
                if (line != ''):
                    rmfile.write(line)
            self.verbose(f"removed part: {self.__opt_dict['rmfile']}")


def usage():
    """show usage"""
    print("""
Usage: python3 Remove_qtrans [options]

    --infile export.xml
         An input xml Wordpress exported file
    --language language_name
         Removing language name. e.g. ja
    -v, --verbose
         verbose mode

Example:
      python3 Remove_qtrans
         --infile    export.xml
         --language  ja
""")
    # raise AssertionError('usage out.')
    sys.exit(1)


def remove_qtrans_main():
    """run remove qtrans
    """
    #
    # command line option handling
    #
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action='store_true',
                        help="Verbose mode.")
    parser.add_argument("--infile", type=str,
                        help="an input wordpress exportex xml file. ")
    parser.add_argument("--outfile", type=str, default="out.xml",
                        help="The output file after current language removal. ")
    parser.add_argument("--rmfile", type=str, default="rm.txt",
                        help="The removed part file. ")
    parser.add_argument("--language", type=str, default="ja",
                        help="removing language section's language name. e.g. ja.")
    args = parser.parse_args()

    if (args.infile == None):
        print("Error: --infile is not specified.")
        usage()

    #
    # Edit following configuration
    #
    opt_dict = {
        'verbose':            args.verbose,
        'infile':             args.infile,
        'outfile':            args.outfile,
        'rmfile':             args.rmfile,
        'language':           args.language,
        }

    csvt = Remove_qtrans(opt_dict)
    csvt.run()


if __name__=="__main__":
    remove_qtrans_main()
