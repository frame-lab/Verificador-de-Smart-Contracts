# ------------------------------------------------------------
# lex.py
#
# tokenizer for a c compiler
# ------------------------------------------------------------

import ply.lex as lex

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

# List of token names.   This is always required
tokens = [
    'INUM',
    'FNUM',
    'ID',
    'LBRACKET',
    'RBRACKET',
    'LBRACE',
    'RBRACE',
    'LPAREN',
    'RPAREN',
    'SEMICOLON',
    'DOT',
    'COMMA',
    'EQUAL',
    'QUOTATION',
    'APOSTROPHE',
    'AMPERSAND',
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

# A regular expression rule with some action code


def t_INUM(t):
    r'\w*'
    t.type = int(t.value)
    return t


def t_FNUM(t):
    r'\w*'
    t.type = float(t.value)
    return t


def t_ID(t):
    r'\w*'
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t

t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = r'\;'
t_DOT = r'\.'
t_COMMA = r'\,'
t_EQUAL = r'\='
t_QUOTATION = r'\"'
t_APOSTROPHE = r'\''
t_AMPERSAND = r'\&'
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

# Error handling rule


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def make_tokens(file):
    lexer = lex.lex()
    file = open("../../Results/tokens.out", "w")
    lexer.input(file)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok: break      # No more input
        file.write(tok)
        tokens.append(tok)
    return tokens
