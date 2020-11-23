class MyJsonRules(object):

    def __init__(self, options):
        self.options = options
        self.err = False

    tokens = [
        'NUMBER',
    ]

    t_ignore = ' \t\n'

    def t_NUMBER(self, t):
        r'-{0,1}\d+'
        value = int(t.value)
        if 'int' in self.options and (value > self.options['int'][1] or value < self.options['int'][0]) or 'positive' in self.options and value < 0:
            print("Illegal character '%s'" % t.value)
            self.err = True
        else:
            t.value = value
            return t

    def t_error(self, t):
        print("Illegal character '%s'" % t.value)
        self.err = True
