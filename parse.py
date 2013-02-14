#!/usr/bin/env python

class Parser(object):
    def __init__(self, filename):
        self.wordChars = [c for c in 'qwertyuiopasdfghjklzxcvbnm']
        self._tex = open(filename).read()
        self._i = 0
        
    def check_current(self, *args):
        return self.get_current() in args

    def get_current(self):
        return self._tex[self._i]

    def next_current(self):
        self._i += 1

    def _read_next(self):
        return self._file.read(1)

    def normal_text(self):
        if self.check_current(' ', *self.wordChars):
            print self.get_current()
            self.next_current()
            self.normal_text()
        elif self.check_current('\\'):
            self.next_current()
            self.command()
            self.normal_text()

    def command(self):
        if self.check_current(*self.wordChars):
            print '   ', self.get_current()
            self.next_current()
            self.command()

if __name__ == '__main__':
    p = Parser('exampleInput/simple.tex')
    p.normal_text()
