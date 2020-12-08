class MyCRules:

    def __init__(self, node):
        self.node = node

    def program_c(self, tree):
        node = self.node(tree.type, None, [])
        for child in tree.children:
            if child.type == 'declist':
                node.set_children(self.node('open_function', '(', []))
                self.declist_c(node.children[0], child, True)
                node.children[0].set_children(
                    self.node('function main', 'None', []))
                node.children[0].set_children(
                    self.node('end_function', ')', []))
            elif child.type == 'funclist':
                self.funclist_c(node, child)
        return node

    def declist_c(self, root, tree, sc):
        for child in tree.children:
            if child.type == 'declaration':
                self.declaration_c(root, child, sc)
            elif child.type == 'declist':
                self.declist_c(root, child, True)

    def funclist_c(self, root, tree):
        for child in tree.children:
            if child.type == 'function':
                self.function_c(root, child)
            elif child.type == 'funclist':
                self.funclist_c(root, child)

    def declaration_c(self, root, tree, sc):
        ident = None
        for child in tree.children:
            if not isinstance(child, str):
                if child.type == 'type':
                    ident = self.type_c(child)
                elif child.type == 'identlist':
                    self.identlist_c(root, child, sc, ident)

    def identlist_c(self, root, tree, sc, ident):
        for child in tree.children:
            if not isinstance(child, str):
                if child.type == 'identlist':
                    self.identlist_c(root, child, True, ident)
                elif child.type == 'identifier':
                    if sc:
                        root.set_children(
                            self.node('expression', "{} {};".format(ident, self.identifier_c(child)), []))
                    else:
                        root.set_children(
                            self.node('expression', "{} {}".format(ident, self.identifier_c(child)), []))

    def identifier_c(self, tree):
        if len(tree.children) == 4:
            return "{}[{}]".format(tree.children[0], tree.children[2])
        else:
            return tree.children[0]

    def paramlist_c(self, root, tree, sc):
        for child in tree.children:
            if not isinstance(child, str):
                if child.type == 'paramlist':
                    self.paramlist_c(root, child, True)
                elif child.type == 'parameter':
                    if sc:
                        root.set_children(
                            self.node('expression', "{};".format(self.parameter_c(child)), []))
                    else:
                        root.set_children(
                            self.node('expression', self.parameter_c(child), []))

    def parameter_c(self, tree):
        return "{} {}".format(self.type_c(tree.children[0]), self.identifier_c(tree.children[1]))

    def function_c(self, root, tree):
        node = self.node('open_function {}'.format(tree.children[1]), '(', [])
        root.set_children(node)
        base_func = root.children[0]
        if base_func.type == 'open_function':
            if len(tree.children) == 6:
                self.paramlist_c(node, tree.children[3], False)
                value = 'main{{{}'.format(
                    node.children[0].value).replace(';', '')
                for i in range(1, len(node.children)):
                    value += ',{}'.format(node.children[i].value.replace(';', ''))
                value += '}'
                base_func.children[-2] = self.node('function main', value, [])
                if len(tree.children[5].children) > 2:
                    node.children[-1].value += ';'
                self.compoundstmt_c(node, tree.children[5])
            elif len(tree.children) == 5:
                base_func.children[-2] = self.node('function main', 'main{}', [])
                self.compoundstmt_c(node, tree.children[4])
        else:
            if len(tree.children) == 6:
                self.paramlist_c(node, tree.children[3], False)
                if len(tree.children[5].children) > 2:
                    node.children[- 1].value += ';'
                self.compoundstmt_c(node, tree.children[5])
            elif len(tree.children) == 5:
                self.compoundstmt_c(node, tree.children[4])
        node.set_children(self.node('end_function', ')', []))

    def type_c(self, tree):
        return tree.children[0]

    def compoundstmt_c(self, root, tree):
        if len(tree.children) == 3:
            if tree.children[1].type == 'stmtlist':
                self.stmtlist_c(root, tree.children[1], False)
            elif tree.children[1].type == 'declist':
                self.declist_c(root, tree.children[1], False)
        elif len(tree.children) == 4:
            self.declist_c(root, tree.children[1], True)
            self.stmtlist_c(root, tree.children[2], False)

    def stmtlist_c(self, root, tree, sc):
        if len(tree.children) == 2:
            if tree.children[1] != ';':
                self.stmtlist_c(root, tree.children[0], True)
            else:
                self.stmtlist_c(root, tree.children[0], sc)
            self.stmt_c(root, tree.children[1], sc)
        elif len(tree.children) == 1:
            self.stmt_c(root, tree.children[0], sc)

    def stmt_c(self, root, tree, sc):
        if not isinstance(tree.children[0], str):
            if tree.children[0].type == 'assignstmt':
                self.assign_c(root, tree.children[0].children[0], sc)
            elif tree.children[0].type == 'callstmt':
                self.node(self.call_c(root, tree.children[0].children[0], sc))
            elif tree.children[0].type == 'retstmt':
                if sc:
                    root.set_children(self.node('expression', '{};'.format(self.retstmt_c(tree.children[0])), []))
                else:
                    root.set_children(self.node('expression', self.retstmt_c(tree.children[0]), []))
            elif tree.children[0].type == 'while':
                self.while_c(root, tree.children[0], sc)
            elif tree.children[0].type == 'for':
                self.for_c(root, tree.children[0], sc)
            elif tree.children[0].type == 'if':
                self.if_c(root, tree.children[0], sc)
            elif tree.children[0].type == 'compoundstmt':
                self.compoundstmt_c(root, tree.children[0])

    def assign_c(self, root, tree, sc):
        if len(tree.children) == 3:
            id = tree.children[0]
            expr = self.expr_c(tree.children[2])
            if sc:
                node = self.node('expression', '{} = {};'.format(id, expr), [])
            else:
                node = self.node('expression', '{} = {}'.format(id, expr), [])
            root.set_children(node)
        if len(tree.children) == 6:
            id = tree.children[0]
            first_expr = self.expr_c(tree.children[2])
            last_expr = self.expr_c(tree.children[5])
            if sc:
                node = self.node('expression', '{}[{}] = {};'.format(
                    id, first_expr, last_expr), [])
            else:
                node = self.node('expression', '{}[{}] = {}'.format(
                    id, first_expr, last_expr), [])
            root.set_children(node)

    def call_c(self, tree, sc):
        call = None
        if len(tree.children) == 3:
            call = self.node('function', '{}()'.format(tree.children[0]), [])
        elif len(tree.children) == 4:
            arg = self.arglist_c(tree.children[2])
            call = '{}({})'.format(tree.children[0], arg)
        return call

    def arglist_c(self, tree):
        arg = None
        if len(tree.children) == 1:
            arg = self.arg_c(tree.children[0])
        elif len(tree.children) == 3:
            arglist = self.arglist_c(tree.children[0])
            arg = '{},{}'.format(arglist, self.arg_c(tree.children[0]))
        return arg

    def arg_c(self, tree):
        return self.expr_c(tree.children[0])

    def retstmt_c(self, tree):
        ret = None
        if len(tree.children) == 2:
            ret = 'return'
        elif len(tree.children) == 3:
            ret = 'return {}'.format(self.expr_c(tree.children[1]))
        return ret

    def expr_c(self, tree):
        expr = None
        if not isinstance(tree, str):
            if len(tree.children) == 3:
                if tree.children[0].type == 'expr':
                    first_expr = self.expr_c(tree.children[0])
                    op = tree.children[1]
                    last_expr = self.expr_c(tree.children[2])
                    expr = "{} {} {}".format(first_expr, op, last_expr)
                else:
                    middle_expr = self.expr_c(tree.children[1])
                    expr = "[{}]".format(middle_expr)
            elif len(tree.children) == 1:
                if isinstance(tree.children[0], int) or isinstance(tree.children[0], float):
                    expr = '{}'.format(tree.children[0])
                elif tree.children[0].type == 'call':
                    expr = '{}'.format(self.call_c(tree.children[0]))
                elif tree.children[0].type == 'id':
                    expr = '{}'.format(self.id_c(tree.children[0]))
            else:
                expr = tree
        return expr

    def id_c(self, tree):
        id = None
        if isinstance(tree.children[0], str):
            id = tree.children[0]
        elif len(tree.children) == 4:
            id = '{}[{}]'.format(tree.children[0],
                                 self.expr_c(tree.children[2]))
        return id

    def while_c(self, root, tree, sc):
        if len(tree.children) == 5:
            while_node = self.node('open_while', '(', [])
            root.set_children(while_node)
            cond_node = self.node('open_while_condition', '(', [])
            expr_node = self.node(
                'expression', '{}{}'.format(self.expr_c(tree.children[2]), '?'), [])
            cond_node.set_children(expr_node)
            cond_node.set_children(self.node('end_condition', ')', []))
            while_node.set_children(cond_node)
            self.stmt_c(while_node, tree.children[4], False)
            if len(while_node.children) > 1:
                cond_node.children[-1].value += ';'
            while_node.set_children(self.node('end_while', ')*', []))
            if sc:
                while_node.set_children(
                    self.node('pos_while', ';', []))
                not_cond_node = self.node('open_while_condition_neg', '(', [])
                expr_node = self.node(
                    'expression', '~{}{}'.format(self.expr_c(tree.children[2]), '?'), [])
                not_cond_node.set_children(expr_node)
                not_cond_node.set_children(
                    self.node('end_condition', ');', []))
                while_node.set_children(not_cond_node)
            else:
                while_node.set_children(
                    self.node('pos_while', ';', []))
                not_cond_node = self.node('open_while_condition_neg', '(', [])
                expr_node = self.node(
                    'expression', '~{}{}'.format(self.expr_c(tree.children[2]), '?'), [])
                not_cond_node.set_children(expr_node)
                not_cond_node.set_children(
                    self.node('end_condition', ')', []))
                while_node.set_children(not_cond_node)
        elif len(tree.children) == 7:
            self.stmt_c(root, tree.children[1], True)
            while_node = self.node('open_while', '(', [])
            root.set_children(while_node)
            cond_node = self.node('open_while_condition', '(', [])
            expr_node = self.node(
                'expression', '{}{}'.format(self.expr_c(tree.children[4]), '?'), [])
            cond_node.set_children(expr_node)
            cond_node.set_children(self.node('end_condition', ')', []))
            while_node.set_children(cond_node)
            self.stmt_c(while_node, tree.children[1], False)
            if len(while_node.children) > 1:
                cond_node.children[-1].value += ';'
            while_node.set_children(self.node('end_while', ')*', []))
            if sc:
                while_node.set_children(
                    self.node('pos_while', ';', []))
                not_cond_node = self.node('open_while_condition_neg', '(', [])
                expr_node = self.node(
                    'expression', '~{}{}'.format(self.expr_c(tree.children[4]), '?'), [])
                not_cond_node.set_children(expr_node)
                not_cond_node.set_children(
                    self.node('end_condition', ');', []))
                while_node.set_children(not_cond_node)
            else:
                while_node.set_children(
                    self.node('pos_while', ';', []))
                not_cond_node = self.node('open_while_condition_neg', '(', [])
                expr_node = self.node(
                    'expression', '~{}{}'.format(self.expr_c(tree.children[4]), '?'), [])
                not_cond_node.set_children(expr_node)
                not_cond_node.set_children(
                    self.node('end_condition', ')', []))
                while_node.set_children(not_cond_node)

    def for_c(self, root, tree, sc):
        self.assign_c(root, tree.children[2], True)
        for_node = self.node('open_for', '(', [])
        root.set_children(for_node)
        cond_node = self.node('open_for_condition', '(', [])
        expr_node = self.node(
            'expression', '{}{}'.format(self.expr_c(tree.children[4]), '?'), [])
        cond_node.set_children(expr_node)
        cond_node.set_children(self.node('end_condition', ');', []))
        for_node.set_children(cond_node)
        self.stmt_c(for_node, tree.children[8], True)
        if len(for_node.children) > 1:
            if len(for_node.children[-1].children) > 0:
                for_node.children[-1].children[-1].children[-1].value += ';'
            else:
                for_node.children[-1].value += ';'
        self.assign_c(for_node, tree.children[6], False)
        for_node.set_children(self.node('end_for', ')*', []))
        if sc:
            for_node.set_children(
                self.node('pos_for', ';', []))
            not_cond_node = self.node('open_for_condition_neg', '(', [])
            expr_node = self.node(
                'expression', '~{}{}'.format(self.expr_c(tree.children[4]), '?'), [])
            not_cond_node.set_children(expr_node)
            not_cond_node.set_children(self.node('end_condition', ');', []))
            for_node.set_children(not_cond_node)
        else:
            for_node.set_children(
                self.node('pos_for', ';', []))
            not_cond_node = self.node('open_for_condition_neg', '(', [])
            expr_node = self.node(
                'expression', '~{}{}'.format(self.expr_c(tree.children[4]), '?'), [])
            not_cond_node.set_children(expr_node)
            not_cond_node.set_children(self.node('end_condition', ')', []))
            for_node.set_children(not_cond_node)

    def if_c(self, root, tree, sc):
        if len(tree.children) == 5:
            if_node = self.node('open_if', '(', [])
            root.set_children(if_node)
            cond_node = self.node('open_if_condition', '(', [])
            expr_node = self.node(
                'expression', '{}{}'.format(self.expr_c(tree.children[2]), '?'), [])
            cond_node.set_children(expr_node)
            cond_node.set_children(self.node('end_condition', ')', []))
            if_node.set_children(cond_node)
            self.stmt_c(if_node, tree.children[4], False)
            if len(if_node.children) > 1:
                cond_node.children[-1].value += ';'
            if_node.set_children(self.node('end_if', ')', []))
            if sc:
                if_node.set_children(
                    self.node('pos_if', 'U'.format(expr_node.value), []))
                not_cond_node = self.node('open_if_condition_neg', '(', [])
                expr_node = self.node(
                    'expression', '~{}{}'.format(self.expr_c(tree.children[2]), '?'), [])
                not_cond_node.set_children(expr_node)
                not_cond_node.set_children(self.node('end_condition', ');', []))
                if_node.set_children(not_cond_node)
            else:
                if_node.set_children(
                    self.node('pos_if', 'U'.format(expr_node.value), []))
                not_cond_node = self.node('open_if_condition_neg', '(', [])
                expr_node = self.node(
                    'expression', '~{}{}'.format(self.expr_c(tree.children[2]), '?'), [])
                not_cond_node.set_children(expr_node)
                not_cond_node.set_children(self.node('end_condition', ')', []))
                if_node.set_children(not_cond_node)
        elif len(tree.children) == 7:
            if_node = self.node('open_if', '(', [])
            root.set_children(if_node)
            cond_node = self.node('open_if_condition', '(', [])
            expr_node = self.node(
                'expression', '{}{}'.format(self.expr_c(tree.children[2]), '?'), [])
            cond_node.set_children(expr_node)
            cond_node.set_children(self.node('end_condition', ')', []))
            if_node.set_children(cond_node)
            self.stmt_c(if_node, tree.children[4], False)
            if len(if_node.children) > 1:
                cond_node.children[-1].value += ';'
            if_node.set_children(self.node('end_if', ')', []))
            if_node.set_children(
                self.node('pos_if', 'U'.format(expr_node.value), []))
            else_node = self.node('open_else', '(', [])
            not_cond_node = self.node('open_if_condition_neg', '(', [])
            expr_node = self.node(
                    'expression', '~{}{}'.format(self.expr_c(tree.children[2]), '?'), [])
            not_cond_node.set_children(expr_node)
            not_cond_node.set_children(self.node('end_condition', ')', []))
            else_node.set_children(not_cond_node)
            if_node.set_children(else_node)
            self.stmt_c(else_node, tree.children[6], False)
            if len(else_node.children) > 1:
                not_cond_node.children[-1].value += ';'
            if sc:
                else_node.set_children(self.node('end_else', ');', []))
            else:
                else_node.set_children(self.node('end_else', ')', []))

    def do_rules(self, tree):
        pdl = self.program_c(tree)
        return pdl
