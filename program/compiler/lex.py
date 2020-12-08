# ------------------------------------------------------------
# lex.py
#
# tokenizer for a c compiler
# ------------------------------------------------------------

import libs.ply.lex as lex
from program.compiler.rules_c.rules_lex import MyCRules
from program.compiler.rules_smacco.rules_lex import MyJsonRules


class MyLexer(object):

    def __init__(self, options, name):
        if options['program'] == 1:
            self.rules = MyCRules(options)
            self.lexer = lex.lex(module=self.rules)
            self.tokens = self.rules.tokens
            self.out = open("./results/minic/{}_token".format(name), "w")
        elif options['program'] == 2:
            self.rules = MyJsonRules(options)
            self.lexer = lex.lex(module=self.rules)
            self.tokens = self.rules.tokens
            self.out = open("./results/smacco/{}_token".format(name), "w")

    def make_tokens(self, data):
        self.lexer.input(data)
        count = 0
        while True:
            tok = self.lexer.token()
            if not tok or self.rules.err:
                break
            if count > 0:
                self.out.write("\n")
            self.out.write(str(tok))
            count += 1
        self.out.close()
        if not self.rules.err:
            print('Suscefully made the tokens for the file')
        return self.rules.err
