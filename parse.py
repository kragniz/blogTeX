#!/usr/bin/env python

class Command(object):
    def __init__(self, name, content=None, args=None):
        self._name = name
        self._content = content
        self._args = args

    def __str__(self):
        return '<Command: "{0}" Args: "{2}"{1}>'.format(
                self.getName(),
                ' Content: "' + ''.join([str(i) for i in self._content]) + '"'
                    if self._content
                    else '',
                self._args
            )

    def getName(self):
        return self._name

class Parser(object):
    def __init__(self, filename):
        self.commandChars = [c for c in '\\{}#$%^&[]']
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

    def next_char(self):
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
                self.next_char()

            elif self.current_is('\\'):
                self.next_char()
                tokens += [self.command()]
            elif inScope and self.current_is('}'):
                self.next_char()
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
        commandArguments = None
        while self.has_more_chars():
            if not self.current_is(' ', *self.commandChars):
                name += self.get_current()
                self.next_char()
            elif self.current_is('{'):
                self.next_char()
                commandContent = self.normal_text(inScope=True)
            elif self.current_is('['):
                self.next_char()
                commandArguments = self.command_arguments()
                print commandArguments
            else:
                break
        return Command(name, content=commandContent,
                                args=commandArguments)



    def command_arguments(self):
        args = {}
        nextArg = True
        def add():
            nextArg = True
            args[argName] = argValue
            #self.next_char()

        while True:
            if nextArg:
                argValue = ''
                argName = None
                nextArg = False

            if not self.current_is('=', ',', *self.commandChars):
                argValue += self.get_current()
                self.next_char()
            elif self.current_is('='):
                argName = argValue
                argValue = ''
                self.next_char()
            elif self.current_is(','):
                add()
            elif self.current_is(' '):
                self.next_char()
            else:
                add()
                self.next_char()
                return args


if __name__ == '__main__':
    p = Parser('exampleInput/simple.tex')
    print ''.join([str(i) for i in p.normal_text()])
