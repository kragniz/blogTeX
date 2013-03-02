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

    @property
    def args(self):
        return self._args

    @property
    def content(self):
        return self._content

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

class Transform(object):
    def __init__(self, tokens, generator):
        self._tokens = tokens
        self._html = ''

        self._generator = generator

    def _run_command(self, command):
        getattr(self._generator, command.name)(command)

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

    @property
    def output(self):
        return self._generator.output

def debug(f):
    def wrapper(*args):
        if args[0]._debug:
            print 'running', f.__name__, 'with', args
        f(*args)
        if args[0]._debug:
            print args[0].__dict__
    return wrapper

class Html(object):
    def __init__(self):
        self._output = ''
        self._debug = False

    @property
    def output(self):
        return self._output

    @debug
    def title(self, c):
        self._title = self._join(c.content)

    @debug
    def author(self, c):
        self._author = self._join(c.content)

    @debug
    def maketitle(self, c):
        self._output += '''<sometag>{title}</sometag>
<someothertag>{author}</someothertag>
'''.format(title = self._title, author = self._author)

    @debug
    def post(self, c):
        print c.args

    @debug
    def tag(self, c):
        self._tags = [tag.strip() for tag in ''.join(c.content).split(',')]

    @debug
    def begin(self, c):
        self._output += '<testenviroment>'

    @debug
    def end(self, c):
        self._output += '</testenviroment>'

    @debug
    def newparagraph(self, c):
        self._output += '''</p>
<p>'''

    def bf(self, c):
        self._output += '<strong>' + self._join(c.content) + '</strong>'

    def _join(self, l):
        return ''.join([str(token) for token in l])

if __name__ == '__main__':
    t = Transform(Lexer('exampleInput/post.tex').normal_text(), Html())
    t.paragraph()
    print t.output
