class MyJsonRules(object):

    def __init__(self, node, tokens):
        self.node = node
        self.tokens = tokens

    def p_program(self, p):
        '''program : NUMBER'''
        if (len(p) == 2):
            p[0] = self.node("program", [p[1]])

    def p_error(self, p):
        if p == None:
            token = "end of file"
        else:
            token = f"{p.type}({p.value}) on line {p.lineno}"

        print(f"Syntax error: Unexpected {token}")
