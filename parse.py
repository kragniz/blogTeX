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

class Lexer(object):
    def __init__(self, filename):
        self.commandChars = [c for c in '\\{}#$%^&[]']
        self._tex = open(filename).read()
        self._fileLength = len(self._tex)
        self._i = 0

        self.tokens = []
        
    def __char_is(self, *args):
        if self.has_more_chars():
            return self.get_current() in args
        else:
            return False

    def get_current(self):
        return self._tex[self._i]

    def __next(self):
        print '%s "%s"' % (self._i, self.get_current())
        self._i += 1

    def has_more_chars(self):
        return self._i < self._fileLength

    def normal_text(self, inScope=False):
        tokens = []
        while self.has_more_chars():
            if not self.__char_is(*self.commandChars):
                tokens += [self.get_current()]
                self.__next()

            elif self.__char_is('\\'):
                self.__next()
                tokens += [self.command()]
            elif inScope and self.__char_is('}'):
                self.__next()
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
            if not self.__char_is(' ', *self.commandChars):
                name += self.get_current()
                self.__next()
            elif self.__char_is('{'):
                self.__next()
                commandContent = self.normal_text(inScope=True)
            elif self.__char_is('['):
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
                argValue += self.get_current()
                self.__next()
            elif _('='):
                argName = argValue
                argValue = ''
                self.__next()

            elif _(','):
                nextArg = True
                args[argName] = argValue
                self.__next()

            elif _(' '): #FIXME this doesn't work for some reason
                self.__next()

            else:
                nextArg = True
                args[argName] = argValue
                self.__next()
                return args


if __name__ == '__main__':
    l = Lexer('exampleInput/simple.tex')
    print ''.join([str(i) for i in p.normal_text()])
