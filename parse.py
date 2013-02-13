#!/usr/bin/env python

import re

class Parser(object):
    def __init__(self, filename):
        self._file = open(filename)

if __name__ == '__main__':
    p = Parser('exampleInput/post.tex')
