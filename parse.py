#!/usr/bin/env python

class Command(object):
    def __init__(self, name):
        self._name = name

    def __str__(self):
        return '<Command: ' + self.getName() + '>'

    def getName(self):
        return self._name

class Parser(object):
    def __init__(self, filename):
        self.commandChars = [c for c in '\\{}#$%^&']
        self._tex = open(filename).read()
        self._fileLength = len(self._tex)
        self._i = 0

        self.tokens = []
        
    def current_is(self, *args):
        if self._i < self._fileLength:
            return self.get_current() in args
        else:
            return False

    def get_current(self):
        return self._tex[self._i]

    def next_current(self):
        self._i += 1

    def has_more_chars(self):
        return self._i < self._fileLength

    def _read_next(self):
        return self._file.read(1)

    def normal_text(self):
        if self.has_more_chars():
            if not self.current_is(*self.commandChars):
                self.tokens += [self.get_current()]
                self.next_current()
                self.normal_text()

            elif self.current_is('\\'):
                self.next_current()
                self.command()
                self.normal_text()

    def command(self, name=''):
        if not self.current_is(' ', *self.commandChars):
            thisChar = self.get_current()
            self.next_current()
            self.command(name + thisChar)
        else:
            self.tokens += [Command(name)]

if __name__ == '__main__':
    p = Parser('exampleInput/simple.tex')
    p.normal_text()
    print ''.join([str(i) for i in p.tokens])
