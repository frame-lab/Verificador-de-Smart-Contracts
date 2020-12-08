class MyCRules(object):

    def __init__(self, node, tokens):
        self.node = node
        self.tokens = tokens

    precedence = (
        ('left', 'LE', 'GE'),
        ('left', 'LT', 'GT'),
        ('left', 'EQ', 'NE'),
        ('left', 'MINUS', 'PLUS'),
        ('left', 'MULT', 'DIV'),
        ('right', 'ID'),
    )

    def p_program(self, p):
        '''program : declist funclist
                   | declist
                   | funclist'''
        if (len(p) == 2):
            p[0] = self.node("program", [p[1]])
        elif (len(p) == 3):
            p[0] = self.node("program", [p[1], p[2]])

    def p_declist(self, p):
        '''declist : declaration
                   | declist declaration'''
        if (len(p) == 2):
            p[0] = self.node("declist", [p[1]])
        elif (len(p) == 3):
            p[0] = self.node("declist", [p[1], p[2]])

    def p_funclist(self, p):
        '''funclist : function
                    | funclist function'''
        if (len(p) == 2):
            p[0] = self.node("funclist", [p[1]])
        elif (len(p) == 3):
            p[0] = self.node("funclist", [p[1], p[2]])

    def p_declaration(self, p):
        'declaration : type identlist SEMICOLON'
        p[0] = self.node("declaration", [p[1], p[2], p[3]])

    def p_identlist(self, p):
        '''identlist : identifier
                     | identlist COMMA identifier'''
        if (len(p) == 2):
            p[0] = self.node("identlist", [p[1]])
        elif (len(p) == 4):
            p[0] = self.node("identlist", [p[1], p[2], p[3]])

    def p_identifier(self, p):
        '''identifier : ID
                      | ID LBRACKET NUMBER RBRACKET'''
        if (len(p) == 2):
            p[0] = self.node("identifier", [p[1]])
        elif (len(p) == 5):
            p[0] = self.node("identifier", [p[1], p[2], p[3], p[4]])

    def p_paramlist(self, p):
        '''paramlist : parameter
                     | paramlist COMMA parameter'''
        if (len(p) == 2):
            p[0] = self.node("paramlist", [p[1]])
        elif (len(p) == 4):
            p[0] = self.node("paramlist", [p[1], p[2], p[3]])

    def p_parameter(self, p):
        'parameter : type identifier'
        p[0] = self.node("parameter", [p[1], p[2]])

    def p_function(self, p):
        '''function : type ID LPAREN RPAREN compoundstmt
                    | type ID LPAREN paramlist RPAREN compoundstmt'''
        if (len(p) == 6):
            p[0] = self.node("function", [p[1], p[2], p[3], p[4], p[5]])
        elif (len(p) == 7):
            p[0] = self.node("function", [p[1], p[2], p[3], p[4], p[5], p[6]])

    def p_type(self, p):
        '''type : INT
                | FLOAT'''
        p[0] = self.node("type", [p[1]])

    def p_compoundstmt(self, p):
        '''compoundstmt : LBRACE RBRACE
                        | LBRACE stmtlist RBRACE
                        | LBRACE declist stmtlist RBRACE
                        | LBRACE declist RBRACE'''
        if (len(p) == 3):
            p[0] = self.node("compoundstmt", [p[1], p[2]])
        elif (len(p) == 4):
            p[0] = self.node("compoundstmt", [p[1], p[2], p[3]])
        elif (len(p) == 5):
            p[0] = self.node("compoundstmt", [p[1], p[2], p[3], p[4]])

    def p_stmtlist(self, p):
        '''stmtlist : stmt
                    | stmtlist stmt'''
        if (len(p) == 2):
            p[0] = self.node("stmtlist", [p[1]])
        elif (len(p) == 3):
            p[0] = self.node("stmtlist", [p[1], p[2]])

    def p_stmt(self, p):
        '''stmt : assignstmt
                | callstmt
                | retstmt
                | while
                | for
                | if
                | compoundstmt
                | SEMICOLON'''
        p[0] = self.node("stmt", [p[1]])

    def p_assignstmt(self, p):
        '''assignstmt : assign SEMICOLON'''
        p[0] = self.node("assignstmt", [p[1], p[2]])

    def p_assign(self, p):
        '''assign : ID EQUAL expr
                  | ID LBRACKET expr RBRACKET EQUAL expr'''
        if (len(p) == 4):
            p[0] = self.node("assign", [p[1], p[2], p[3]])
        elif (len(p) == 7):
            p[0] = self.node("assign", [p[1], p[2], p[3], p[4], p[5], p[6]])

    def p_callstmt(self, p):
        '''callstmt : call SEMICOLON'''
        p[0] = self.node("callstmt", [p[1], p[2]])

    def p_call(self, p):
        '''call : ID LPAREN RPAREN
                | ID LPAREN arglist RPAREN'''
        if (len(p) == 4):
            p[0] = self.node("call", [p[1], p[2], p[3]])
        elif (len(p) == 5):
            p[0] = self.node("call", [p[1], p[2], p[3], p[4]])

    def p_arglist(self, p):
        '''arglist : arg
                   | arglist COMMA arg'''
        if (len(p) == 2):
            p[0] = self.node("arglist", [p[1]])
        elif (len(p) == 4):
            p[0] = self.node("arglist", [p[1], p[2], p[3]])

    def p_arg(self, p):
        '''arg : expr'''
        p[0] = self.node("arg", [p[1]])

    def p_retstmt(self, p):
        '''retstmt : RETURN SEMICOLON
                   | RETURN expr SEMICOLON'''
        if (len(p) == 3):
            p[0] = self.node("retstmt", [p[1], p[2]])
        elif (len(p) == 4):
            p[0] = self.node("retstmt", [p[1], p[2], p[3]])

    def p_expr(self, p):
        '''expr : expr MINUS expr
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
                | NUMBER
                | FNUMBER
                | id
                | LPAREN expr RPAREN'''
        if (len(p) == 2):
            p[0] = self.node("expr", [p[1]])
        elif (len(p) == 3):
            p[0] = self.node("expr", [p[1], p[2]])
        elif (len(p) == 4):
            p[0] = self.node("expr", [p[1], p[2], p[3]])

    def p_id(self, p):
        '''id : ID
              | ID LBRACKET expr RBRACKET'''
        if (len(p) == 2):
            p[0] = self.node("id", [p[1]])
        elif (len(p) == 5):
            p[0] = self.node("id", [p[1], p[2], p[3], p[4]])

    def p_while(self, p):
        '''while : WHILE LPAREN expr RPAREN stmt
                 | DO stmt WHILE LPAREN expr RPAREN SEMICOLON'''
        if (len(p) == 6):
            p[0] = self.node("while", [p[1], p[2], p[3], p[4], p[5]])
        elif (len(p) == 8):
            p[0] = self.node("while", [p[1], p[2], p[3], p[4], p[5], p[6], p[7]])

    def p_for(self, p):
        '''for : FOR LPAREN assign SEMICOLON expr SEMICOLON assign RPAREN stmt'''
        p[0] = self.node("for", [p[1], p[2], p[3], p[4],
                            p[5], p[6], p[7], p[8], p[9]])

    def p_if(self, p):
        '''if : IF LPAREN expr RPAREN stmt
              | IF LPAREN expr RPAREN stmt ELSE stmt'''
        if (len(p) == 6):
            p[0] = self.node("if", [p[1], p[2], p[3], p[4], p[5]])
        elif (len(p) == 8):
            p[0] = self.node("if", [p[1], p[2], p[3], p[4], p[5], p[6], p[7]])

    def p_error(self, p):
        if p == None:
            token = "end of file"
        else:
            token = f"{p.type}({p.value}) on line {p.lineno}"

        print(f"Syntax error: Unexpected {token}")