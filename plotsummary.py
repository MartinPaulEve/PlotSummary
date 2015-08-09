#!/usr/bin/env python
# Plots various graphs for a series of plaintext files in a directory
# Copyright Martin Paul Eve 2015

"""plotsummary: Plots various graphs for a series of plaintext files in a directory

Usage:
    plotsummary.py single <directory> <term_file> [options]
    plotsummary.py hist <directory> <term_file> [options]
    plotsummary.py group <directory> <term_file> <term_name> <second_term_file> <second_term_name> [options]
    plotsummary.py rawcount <directory> <term_file> [options]
    plotsummary.py (-h | --help)
    plotsummary.py --version

Options:
    -c, --caption <caption>                         Specify the output caption
    -d, --debug                                     Enable debug output
    -h --help                                       Show this screen.
    -n, --nostem <nostem>                           Specify a path containing words that should not be stemmed
    --version                                       Show version.
"""

import os
from os import listdir
from os.path import isfile, join
from text import Text
import re
from debug import Debug, Debuggable
from docopt import docopt
from interactive import Interactive
import subprocess


class KernelDensity (Debuggable):
    def __init__(self):
        # read  command line arguments
        self.args = self.read_command_line()

        # absolute first priority is to initialize debugger so that anything triggered here can be logged
        self.debug = Debug()

        Debuggable.__init__(self, 'plotsummary')

        self.in_dir = self.args['<directory>']
        self.term_file = self.args['<term_file>']

        self.terms = [line.strip() for line in open(self.term_file)]

        self.dir = os.path.dirname(os.path.abspath(__file__))

        if self.args['--debug']:
            self.debug.enable_debug()

        self.debug.enable_prompt(Interactive(self.args['--debug']))

        if self.args['--caption']:
            self.caption = self.args['--caption']
        else:
            self.caption = 'Term Plot'

        if self.args['--nostem']:
            self.nostem = self.args['--nostem']
        else:
            self.nostem = None

        if self.args['single']:
            self.action = 'single'
        elif self.args['group']:
            self.second_term_file = self.args['<second_term_file>']
            self.term_name = self.args['<term_name>']
            self.second_term_name = self.args['<second_term_name>']
            self.second_terms = [line.strip() for line in open(self.second_term_file)]
            self.action = 'group'
        elif self.args['hist']:
            self.action = 'hist'
        elif self.args['rawcount']:
            self.action = 'rawcount'

    @staticmethod
    def read_command_line():
        return docopt(__doc__, version='kernel-density-estimation v0.1')

    def run(self):
        if self.args['--debug']:
            if self.nostem:
                with open(self.nostem) as f:
                    nostem_words = set(f.read().splitlines())

            for term in self.terms:
                if not term in nostem_words:
                    self.debug.print_debug(self, u'{0} will be stemmed to {1}'.format(term, Text.show_stem(term)))
                else:
                    self.debug.print_debug(self, u'{0} will not be stemmed'.format(term))

            if self.action == 'group':
                for term in self.second_terms:
                    if not term in nostem_words:
                        self.debug.print_debug(self, u'{0} will be stemmed to {1}'.format(term, Text.show_stem(term)))
                    else:
                        self.debug.print_debug(self, u'{0} will not be stemmed'.format(term))

        file_list = listdir(self.in_dir)

        for file_name in file_list:
            if file_name.endswith(".txt"):
                self.plot(file_name)

    def plot(self, file_name):
        self.debug.print_debug(self, u'Loading ' + file_name)
        textplot = Text.from_file(join(self.in_dir, file_name), self.debug, nostem=self.nostem)

        self.debug.print_debug(self, u'Plotting ' + file_name)
        if self.action == 'single':
            graph = textplot.plot_terms(self.terms, self.caption)

        elif self.action == 'group':
            graph = textplot.plot_terms_two_groups(self.terms, self.term_name, self.second_terms,self.second_term_name, self.caption)

        elif self.action == 'hist':
            graph = textplot.plot_terms_histogram(self.terms, self.caption, 5000)
        elif self.action == 'rawcount':
            graph = textplot.plot_terms_raw_count(self.terms, self.caption, 5000)

        self.debug.print_debug(self, u'Saving ' + file_name.replace('.txt', '.png'))
        graph.savefig(join(self.in_dir, file_name.replace('.txt', '.png')))

        graph.close()

def main():
    cwf_instance = KernelDensity()
    cwf_instance.run()

if __name__ == '__main__':
    main()