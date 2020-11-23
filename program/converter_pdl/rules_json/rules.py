import os


class Node:
    def __init__(self, children=None, parent=[]):
        self.children = children
        self.parent = parent


class MyJsonRules:
    def program_p(self, parser, node):
        return node

    def declist_p(self, parser, node):
        return node

    def funclist_p(self, parser, node):
        return node

    def declaration_p(self, parser, node):
        return node

    def identlist_p(self, parser, node):
        return node

    def identifier_p(self, parser, node):
        return node

    def paramlist_p(self, parser, node):
        return node

    def parameter_p(self, parser, node):
        return node

    def function_p(self, parser, node):
        return node

    def type_p(self, parser, node):
        return node

    def compoundstmt_p(self, parser, node):
        return node

    def stmtlist_p(self, parser, node):
        return node

    def stmt_p(self, parser, node):
        return node

    def assignstmt_p(self, parser, node):
        return node

    def assign_p(self, parser, node):
        return node

    def callstmt_p(self, parser, node):
        return node

    def call_p(self, parser, node):
        return node

    def arglist_p(self, parser, node):
        return node

    def arg_p(self, parser, node):
        return node

    def retstmt_p(self, parser, node):
        return node

    def expr_p(self, parser, node):
        return node

    def id_p(self, parser, node):
        return node

    def while_p(self, parser, node):
        return node

    def for_p(self, parser, node):
        return node

    def if_p(self, parser, node):
        return node

    def do_rules(self, tree):
        pdl = self.program_p(tree, Node())
        return pdl