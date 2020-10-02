# ------------------------------------------------------------
# yacc.py
#
# parsing for a c compiler
# ------------------------------------------------------------

import ply.yacc as yacc
 
# Get the token map from the lexer.  This is required.
from lex import tokens

def p_program(p):
    '''program : declist funclist
               | declist
               | funclist'''

def p_declist(p):
    '''declist : declaration
               | declist declaration'''

def p_funclist(p):
    '''funclist : function
                | funclist function'''
 
def p_declaration(p):
    'declaration : type identlist SEMICOLON'

def p_identlist(p):
    '''identlist : identifier
                 | identlist COMMA identifier'''

def p_identifier(p):
    '''identifier : ID
                  | ID LBRACKER INUM RBRACKET'''

def p_paramlist(p):
    '''paramlist : parameter
                 | paramlist COMMA parameter'''

def p_parameter(p):
    'parameter : type identifier'

def p_function(p):
    '''function : type ID LPAREN RPAREN compoundstmt
                | type ID LPAREN paramlist RPAREN compoundstmt'''

def p_type(p):
    '''type : INUM
            | FNUM'''

def p_compoundstmt(p):
    '''type : LBRACE RBRACE
            | LBRACE stmtlist RBRACE
            | LBRACE declist stmtlist Rbrace
            | LBRACE declist Rbrace'''

def p_stmtlist(p):
    '''stmtlist : stmt
            | stmtlist stmt'''

def p_stmt(p):
    '''stmt : assignstmt
            | callstmt
            | retstmt
            | while
            | for
            | if
            | compoundstmt
            | SEMICOLON'''

def p_assignstmt(p):
    '''assignstmt : assign SEMICOLON'''

def p_assign(p):
    '''assign : ID EQUAL expr
              | ID LBRACKET expr RBRACKET EQUAL expr'''

def p_callstmt(p):
    '''callstmt : call SEMICOLON'''

def p_call(p):
    '''call : ID LPAREN RPAREN
            | ID LPAREN arglist RPAREN'''

def p_arglist(p):
    '''arglist : arg
               | arglist COMMA arg'''
 
def p_arg(p):
    '''arg : expr'''

def p_retstmt(p):
    '''retstmt : RETURN SEMICOLON
               | RETURN expr SEMICOLON'''

def p_expr(p):
    '''expr : MINUS expr
            | expr MINUS expr
            | expr PLUS expr
            | expr MULT expr
            | expr DIV expr
            | expr LE expr
            | expr GE expr
            | expr GT expr
            | expr LT expr
            | expr EQ expr
            | expr NE expr
            | call
            | type
            | ID
            | LPAREN expr RPAREN'''

def p_id(p):
    '''id : ID
        | ID LBRACKET expr RBRACKET'''


def p_while(p):
    '''while : WHILE LPAREN expr RPAREN stmt
             | DO stmt WHILE LPAREN expr RPAREN SEMICOLON'''

def p_for(p):
    '''for : FOR LPAREN assign SEMICOLON expr SEMICOLON assign LPAREN stmt'''

def p_if(p):
    '''if : IF LPAREN expr RPAREN stmt
          | IF LPAREN expr RPAREN stmt ELSE stmt'''

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")


def make_parser(file):
    parser = yacc.yacc()
    file = open("../../Results/parser.out", "w")
    while True:
        if not file: continue
        result = parser.parse(file)
        file.write(result)
    return parser
