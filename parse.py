#!/usr/bin/env python

class Command(object):
    def __init__(self, name, content=None, args=None):
        self._name = name
        self._content = content
        self._args = args

    def __str__(self):
        return '<Command: "{0}" Args: "{2}"{1}>'.format(
                self.name,
                ' Content: "' + ''.join([str(i) for i in self._content]) + '"'
                    if self._content
                    else '',
                self._args
            )

    @property
    def name(self):
        return self._name

class Lexer(object):
    def __init__(self, filename):
        self.commandChars = [c for c in '\\{}#$%^&[]']
        self._tex = open(filename).read()
        self._fileLength = len(self._tex)
        self._i = 0

        self.tokens = []
        
    def __char_is(self, *args):
        if self.has_more_chars():
            return self.get() in args
        else:
            return False

    def get(self, offset=0):
        '''Return the character at the current location. Use offset to get the
        next or previous character'''
        def _get(): return self._tex[self._i + offset]
        if _get() == '%':
            while _get() != '\n':
                self.__next()
        return _get()

    def __next(self):
        self._i += 1

    def has_more_chars(self):
        return self._i < self._fileLength

    def normal_text(self, inScope=False):
        tokens = []
        _ = self.__char_is
        while self.has_more_chars():
            if not _(*self.commandChars):
                tokens += [self.get()]
                self.__next()
            elif _('\\'):
                self.__next()
                tokens += [self.command()]
            elif inScope and _('}'):
                self.__next()
                return tokens
            else:
                raise IOError(
                    'I\'m not sure what to do with the character "%s"' %
                    self.get()
                )
        return tokens

    def command(self):
        name = ''
        commandContent = None
        commandArguments = None
        _ = self.__char_is
        while self.has_more_chars():
            if not _(' ', '\n', *self.commandChars):
                name += self.get()
                self.__next()
            elif _('{'):
                self.__next()
                commandContent = self.normal_text(inScope=True)
            elif _('['):
                self.__next()
                commandArguments = self.command_arguments()
            else:
                break
        return Command(name,
                       content=commandContent,
                       args=commandArguments)

    def command_arguments(self):
        args = {}
        nextArg = True
        _ = self.__char_is
        while self.has_more_chars():
            if nextArg:
                argValue = ''
                argName = None
                nextArg = False

            if not _('=', ',', *self.commandChars):
                argValue += self.get()
                self.__next()

            elif _('='):
                argName = argValue
                argValue = ''
                self.__next()

            elif _(','):
                nextArg = True
                args[argName] = argValue
                self.__next()

            else:
                args[argName.strip()] = argValue.strip()
                self.__next()
                return args

class Transform(object):
    def __init__(self, tokens):
        self._tokens = tokens
        self._html = ''

    def paragraph(self):
        lastChar = ''
        for t in self._tokens:
            if type(t) is Command:
                print t.name
            else:
                if not (t == ' ' and lastChar == ' '):
                    print '"%s"' % t
                else: pass
                lastChar = t

if __name__ == '__main__':
    t = Transform(Lexer('exampleInput/post.tex').normal_text())
    t.paragraph()
