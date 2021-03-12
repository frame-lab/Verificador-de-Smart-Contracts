class MyCRules(object):

    def __init__(self, options):
        self.options = options
        self.err = False

    reserved = {
        'int': 'INT',
        'float': 'FLOAT',
        'if': 'IF',
        'else': 'ELSE',
        'for': 'FOR',
        'while': 'WHILE',
        'do': 'DO',
        'return': 'RETURN',
    }

    tokens = [
        'NUMBER',
        'FNUMBER',
        'ID',
        'LBRACKET',
        'RBRACKET',
        'LBRACE',
        'RBRACE',
        'LPAREN',
        'RPAREN',
        'SEMICOLON',
        'COMMA',
        'EQUAL',
        'MINUS',
        'PLUS',
        'MULT',
        'DIV',
        'LE',
        'GE',
        'GT',
        'LT',
        'EQ',
        'NE',
    ] + list(reserved.values())

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

    def t_FNUMBER(self, t):
        r'-{0,1}\d+,\d+'
        value = float(t.value)
        if 'int' in self.options and (value > self.options['int'][1] or value < self.options['int'][0]) or 'positive' in self.options and value < 0:
            print("Illegal character '%s'" % t.value)
            self.err = True
        else:
            t.value = value
            return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'ID')
        return t

    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_SEMICOLON = r'\;'
    t_COMMA = r'\,'
    t_EQUAL = r'\='
    t_MINUS = r'\-'
    t_PLUS = r'\+'
    t_MULT = r'\*'
    t_DIV = r'\/'
    t_LE = r'<='
    t_GE = r'>='
    t_GT = r'>'
    t_LT = r'<'
    t_EQ = r'=='
    t_NE = r'!='

    def t_error(self, t):
        print("Illegal character '%s'" % t.value)
        self.err = True
