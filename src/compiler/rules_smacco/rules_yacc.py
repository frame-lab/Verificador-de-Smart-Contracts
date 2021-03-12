class MyJsonRules(object):

    def __init__(self, node, tokens):
        self.node = node
        self.tokens = tokens

    def p_program(self, p):
        '''program : LBRACE RBRACE
                   | LBRACE paramlist RBRACE'''
        if (len(p) == 3):
            p[0] = self.node("program", [p[1], p[2]])
        elif (len(p) == 4):
            p[0] = self.node("program", [p[1], p[2], p[3]])

    def p_paramlist(self, p):
        '''paramlist : param
                     | paramlist COMMA param'''
        if (len(p) == 2):
            p[0] = self.node("paramlist", [p[1]])
        elif (len(p) == 4):
            p[0] = self.node("paramlist", [p[1], p[2], p[3]])

    def p_param(self, p):
        '''param : QUOT type QUOT COLON expression'''
        if (len(p) == 6):
            p[0] = self.node("param", [p[1], p[2], p[3], p[4], p[5]])

    def p_type(self, p):
        '''type : STANDARD
                | INPUT_TYPE
                | PUBKEY_LIST
                | RULE
                | RULES
                | DEFAULT_RULE
                | INLINE_LAST'''
        if (len(p) == 2):
            p[0] = self.node("type", [p[1]])

    def p_expression(self, p):
        '''expression : variable
                      | list
                      | object'''
        if (len(p) == 2):
            p[0] = self.node("expression", [p[1]])

    def p_variable(self, p):
        '''variable : QUOT input QUOT'''
        if (len(p) == 4):
            p[0] = self.node("variable", [p[1], p[2], p[3]])

    def p_input(self, p):
        '''input : SINGLE
                 | ARRAY
                 | SMACCO
                 | DISABLED
                 | ALLOW_ALL
                 | DENY_ALL'''
        if (len(p) == 2):
            p[0] = self.node("input", [p[1]])

    def p_list(self, p):
        '''list : LBRACKET RBRACKET
                | LBRACKET listparamlist RBRACKET'''
        if (len(p) == 3):
            p[0] = self.node("list", [p[1], p[2]])
        elif (len(p) == 4):
            p[0] = self.node("list", [p[1], p[2], p[3]])

    def p_listparamlist(self, p):
        '''listparamlist : listparam
                         | listparamlist COMMA listparam'''
        if (len(p) == 2):
            p[0] = self.node("listparamlist", [p[1]])
        elif (len(p) == 4):
            p[0] = self.node("listparamlist", [p[1], p[2], p[3]])

    def p_listparam(self, p):
        '''listparam : object
                     | QUOT ID QUOT'''
        if (len(p) == 2):
            p[0] = self.node("listparam", [p[1]])
        elif (len(p) == 4):
            p[0] = self.node("listparam", [p[1], p[2], p[3]])

    def p_object(self, p):
        '''object : LBRACE RBRACE
                  | LBRACE objectparamlist RBRACE'''
        if (len(p) == 3):
            p[0] = self.node("object", [p[1], p[2]])
        elif (len(p) == 4):
            p[0] = self.node("object", [p[1], p[2], p[3]])

    def p_objectparamlist(self, p):
        '''objectparamlist : objectparam
                           | objectparamlist COMMA objectparam'''
        if (len(p) == 2):
            p[0] = self.node("objectparamlist", [p[1]])
        elif (len(p) == 4):
            p[0] = self.node("objectparamlist", [p[1], p[2], p[3]])

    def p_objectparam(self, p):
        '''objectparam : QUOT objecttype QUOT COLON objectexpression'''
        if (len(p) == 6):
            p[0] = self.node("objectparam", [p[1], p[2], p[3], p[4], p[5]])

    def p_objecttype(self, p):
        '''objecttype : RULE_TYPE 
                      | CONDITION'''
        if (len(p) == 2):
            p[0] = self.node("objecttype", [p[1]])

    def p_objectexpression(self, p):
        '''objectexpression : objectvariable 
                            | objectcondition'''
        if (len(p) == 2):
            p[0] = self.node("objectexpression", [p[1]])

    def p_objectvariable(self, p):
        '''objectvariable : QUOT objectinput QUOT'''
        if (len(p) == 4):
            p[0] = self.node("objectvariable", [p[1], p[2], p[3]])

    def p_objectinput(self, p):
        '''objectinput : ALLOW_IF 
                       | DENY_IF'''
        if (len(p) == 2):
            p[0] = self.node("objectinput", [p[1]])

    def p_objectcondition(self, p):
        '''objectcondition : LBRACE RBRACE 
                           | LBRACE conditionparamlist RBRACE'''
        if (len(p) == 3):
            p[0] = self.node("objectcondition", [p[1], p[2]])
        elif (len(p) == 4):
            p[0] = self.node("objectcondition", [p[1], p[2], p[3]])

    def p_conditionparamlist(self, p):
        '''conditionparamlist : conditionparam
                              | conditionparamlist COMMA conditionparam'''
        if (len(p) == 2):
            p[0] = self.node("conditionparamlist", [p[1]])
        elif (len(p) == 4):
            p[0] = self.node("conditionparamlist", [p[1], p[2], p[3]])

    def p_conditionparam(self, p):
        '''conditionparam : QUOT conditiontype QUOT COLON conditionexpression'''
        if (len(p) == 6):
            p[0] = self.node("conditionparam", [p[1], p[2], p[3], p[4], p[5]])

    def p_conditiontype(self, p):
        '''conditiontype : CONDITION_TYPE
                         | CONDITION_NAME
                         | PUBKEY
                         | PUBKEYS
                         | SIGNATURES
                         | MINIMUM_REQUIRED
                         | CONDITIONS
                         | TIMESTAMP
                         | UTC'''
        if (len(p) == 2):
            p[0] = self.node("conditiontype", [p[1]])

    def p_conditionexpression(self, p):
        '''conditionexpression : conditionvariable
                               | conditionlist'''
        if (len(p) == 2):
            p[0] = self.node("conditionexpression", [p[1]])

    def p_conditionvariable(self, p):
        '''conditionvariable : QUOT ID QUOT'''
        if (len(p) == 4):
            p[0] = self.node("conditionvariable", [p[1], p[2], p[3]])

    def p_conditionlist(self, p):
        '''conditionlist : LBRACKET RBRACKET 
                         | LBRACKET conditionlistparamlist RBRACKET'''
        if (len(p) == 3):
            p[0] = self.node("conditionlist", [p[1], p[2]])
        elif (len(p) == 4):
            p[0] = self.node("conditionlist", [p[1], p[2], p[3]])

    def p_conditionlistparamlist(self, p):
        '''conditionlistparamlist : conditionlistparam
                                  | conditionlistparamlist COMMA conditionlistparam'''
        if (len(p) == 2):
            p[0] = self.node("conditionlistparamlist", [p[1]])
        elif (len(p) == 4):
            p[0] = self.node("conditionlist", [p[1], p[2], p[3]])

    def p_conditionlistparam(self, p):
        '''conditionlistparam : objectcondition 
                              | QUOT ID QUOT'''
        if (len(p) == 2):
            p[0] = self.node("conditionlistparam", [p[1]])
        elif (len(p) == 4):
            p[0] = self.node("conditionlistparam", [p[1], p[2], p[3]])

    def p_error(self, p):
        if p == None:
            token = "end of file"
        else:
            token = f"{p.type}({p.value}) on line {p.lineno}"

        print(f"Syntax error: Unexpected {token}")
