# ------------------------------------------------------------
# yacc.py
#
# parsing for a c compiler
# ------------------------------------------------------------

import libs.ply.yacc as yacc
from src.compiler.lex import MyLexer
from src.compiler.rules_c.rules_yacc import MyCRules
from src.compiler.rules_smacco.rules_yacc import MyJsonRules


class Node:
    def __init__(self, type, children):
        self.type = type
        self.children = children

    def __str__(self):
        return "type = {}, children = {}\n".format(self.type, self.children)

    def __repr__(self):
        return self.type


class MyCompiler(object):

    def __init__(self, options, name):
        self.lexer = MyLexer(options, name)
        if options['program'] == 1:
            self.parser = yacc.yacc(module=MyCRules(Node, self.lexer.tokens))
            self.out = open("./results/{}_parser".format(name), "w")
        if options['program'] == 2:
            self.parser = yacc.yacc(module=MyJsonRules(Node, self.lexer.tokens))
            self.out = open("./results/{}_parser".format(name), "w")

    def write_file(self, out, node):
        out.write(node.__str__())
        if node != None:
            for child in node.children:
                if isinstance(child, Node):
                    self.write_file(out, child)

    def make_parser(self, data):
        result = self.lexer.make_tokens(data)
        if not result:
            tree = self.parser.parse(data)
            if tree:
                self.write_file(self.out, tree)
                print('Suscefully parsed the file')
            self.out.close()
            return tree
        else:
            self.out.close()
            return None
