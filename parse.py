#!/usr/bin/env python

class Command(object):
    def __init__(self, name, content=None, args=None):
        self._name = name
        self._content = content
        self._args = args

    def __str__(self):
        return '<Command: "{0}" Args: "{2}"{1}>'.format(
                self.name,
                ' Content: "' + _join(self._content) + '"'
                    if self._content
                    else '',
                self._args
            )

    @property
    def name(self):
        return self._name

    @property
    def args(self):
        return self._args

    @property
    def content(self):
        return self._content

class Lexer(object):
    def __init__(self, filename):
        self.commandChars = list('\\{}#$%^&[]')
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
                self.__next()
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

def _join(l):
    return ''.join(str(i) for i in l)

class Post(object):
    def __init__(self, date, title):
        self.date = date
        self.title = title

    def __str__(self):
        return '<Post date=' + self.date + ' title="' + _join(self.title) + '"'

class Transform(object):
    def __init__(self, tokens):
        self._tokens = tokens
        self._html = ''
        self._metadata = {'tags': []}
        self._posts = []
        self._scope = []

    def _run_command(self, command):
        getattr(self, command.name)(command)

    def paragraph(self):
        lastChar = ''
        for t in self._tokens:
            if type(t) is Command:
                self._run_command(t)
            else:
                if t == '\n':
                    if lastChar == '\n':
                        self._run_command(Command('newparagraph'))
                elif not (t == ' ' and lastChar == ' '):
                    pass
                    #print '"%s"' % t
                else: pass
                lastChar = t

    def title(self, c):
        self._metadata['title'] = _join(c.content)

    def author(self, c):
        self._metadata['author'] = _join(c.content)

    def newparagraph(self, c):
        pass

    def maketitle(self, c):
        print self._metadata

    def post(self, c):
        self._posts += [Post(c.args['date'], c.content)]

    def tag(self, c):
        self._metadata['tags'] += [tag.strip() for tag in _join(c.content).split(',')]

    def begin(self, c):
        self._scope += _join(c.content)

    def end(self, c):
        self._scope.pop()

if __name__ == '__main__':
    t = Transform(Lexer('exampleInput/post.tex').normal_text())
    print t.paragraph()
