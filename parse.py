#!/usr/bin/env python

class Command(object):
    def __init__(self, name, content=None):
        self._name = name
        self._content = content

    def __str__(self):
        return '<Command: "{0}"{1}>'.format(
                self.getName(),
                ' Content: "' + ''.join([str(i) for i in self._content]) + '"'
                    if self._content
                    else ''
            )

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
        print self._i, self.get_current()
        self._i += 1

    def has_more_chars(self):
        return self._i < self._fileLength

    def _read_next(self):
        return self._file.read(1)

    def normal_text(self, inScope=False):
        tokens = []
        while self.has_more_chars():
            if not self.current_is(*self.commandChars):
                tokens += [self.get_current()]
                self.next_current()

            elif self.current_is('\\'):
                self.next_current()
                tokens += [self.command()]
            elif inScope and self.current_is('}'):
                self.next_current()
                return tokens
            else:
                raise IOError(
                    'I\'m not sure what to do with the character "%s"' %
                    self.get_current()
                )
        return tokens

    def command(self):
        name = ''
        commandContent = None
        while True:
            if not self.current_is(' ', *self.commandChars):
                thisChar = self.get_current()
                self.next_current()
                name += thisChar
            elif self.current_is('{'):
                self.next_current()
                commandContent = self.normal_text(inScope=True)
            else:
                return Command(name, content=commandContent)

if __name__ == '__main__':
    p = Parser('exampleInput/simple.tex')
    print ''.join([str(i) for i in p.normal_text()])
