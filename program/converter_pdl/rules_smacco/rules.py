class MySmaccoRules:

    def __init__(self, node):
        self.node = node

    def program_c(self, tree):
        node = self.node(tree.type, None, [])
        node.set_children(self.node('open_function main', '(', []))
        if not isinstance(tree.children[1], str):
            self.paramlist_c(node.children[0], tree.children[1], False)
        node.children[0].set_children(
                    self.node('end_function', ')', []))
        return node

    def paramlist_c(self, root, tree, sc):
        for child in tree.children:
            if not isinstance(child, str):
                if child.type == 'paramlist':
                    self.paramlist_c(root, child, True)
                elif child.type == 'param':
                    self.param_c(root, child, sc)
    
    def param_c(self, root, tree, sc):
        ident = self.type_c(tree.children[1])
        self.expression_c(root, tree.children[4], sc, ident)

    def type_c(self, tree):
        return tree.children[0]

    def expression_c(self, root, tree, sc, ident):
        if tree.children[0].type == 'variable':
            self.variable_c(root, tree.children[0], sc, ident)
        elif tree.children[0].type == 'list':
            self.list_c(root, tree.children[0], sc, ident)
        elif tree.children[0].type == 'object':
            self.object_c(root, tree.children[0], sc)

    def variable_c(self, root, tree, sc, ident):
        if sc:
            root.set_children(self.node('expression', '{} = {};'.format(ident, self.input_c(tree.children[1])), []))
        else:
            root.set_children(self.node('expression', '{} = {}'.format(ident, self.input_c(tree.children[1])), []))

    def input_c(self, tree):
        return tree.children[0]

    def list_c(self, root, tree, sc, ident):
        if not isinstance(tree.children[1], str):
            self.listparamlist_c(root, tree.children[1], sc, ident)

    def listparamlist_c(self, root, tree, sc, ident):
        for child in tree.children:
            if not isinstance(child, str):
                if child.type == 'listparamlist':
                    self.listparamlist_c(root, child, True, ident)
                elif child.type == 'listparam':
                    self.listparam_c(root, child, sc, ident)

    def listparam_c(self, root, tree, sc, ident):
        for child in tree.children:
            if not isinstance(child, str):
                if child.type == 'object':
                    self.object_c(root, child, sc)
            elif isinstance(child, str) and child != '"':
                if sc:
                    root.set_children(self.node('expression', '{} = {};'.format(ident, tree.children[1]), []))
                else:
                    root.set_children(self.node('expression', '{} = {}'.format(ident, tree.children[1]), []))

    def object_c(self, root, tree, sc):
        if not isinstance(tree.children[1], str):
            self.objectparamlist_c(root, tree.children[1], sc)

    def objectparamlist_c(self, root, tree, sc):
        for child in tree.children:
            if not isinstance(child, str):
                if child.type == 'objectparamlist':
                    self.objectparamlist_c(root, child, True)
                elif child.type == 'objectparam':
                    self.objectparam_c(root, child, sc)

    def objectparam_c(self, root, tree, sc):
        ident = self.objecttype_c(tree.children[1])
        self.objectexpression_c(root, tree.children[4], sc, ident)

    def objecttype_c(self, tree):
        return tree.children[0]

    def objectexpression_c(self, root, tree, sc, ident):
        if tree.children[0].type == 'objectvariable':
            self.objectvariable_c(root, tree.children[0], sc, ident)
        elif tree.children[0].type == 'objectcondition':
            self.objectcondition_c(root, tree.children[0], sc)

    def objectvariable_c(self, root, tree, sc, ident):
        if sc:
            root.set_children(self.node('expression', '{} = {};'.format(ident, self.objectinput_c(tree.children[1])), []))
        else:
            root.set_children(self.node('expression', '{} = {}'.format(ident, self.objectinput_c(tree.children[1])), []))
            
    def objectinput_c(self, tree):
        return tree.children[0]

    def objectcondition_c(self, root, tree, sc):
        if not isinstance(tree.children[1], str):
            self.conditionparamlist_c(root, tree.children[1], sc)

    def conditionparamlist_c(self, root, tree, sc):
        for child in tree.children:
            if not isinstance(child, str):
                if child.type == 'conditionparamlist':
                    self.conditionparamlist_c(root, child, True)
                elif child.type == 'conditionparam':
                    self.conditionparam_c(root, child, sc)

    def conditionparam_c(self, root, tree, sc):
        ident = self.conditiontype_c(tree.children[1])
        self.conditionexpression_c(root, tree.children[4], sc, ident)

    def conditiontype_c(self, tree):
        return tree.children[0]

    def conditionexpression_c(self, root, tree, sc, ident):
        if tree.children[0].type == 'conditionvariable':
            if sc:
                root.set_children(self.node('expression', '{} = {};'.format(ident, self.conditionvariable_c(tree.children[0])), []))
            else:
                root.set_children(self.node('expression', '{} = {}'.format(ident, self.conditionvariable_c(tree.children[0])), []))
        elif tree.children[0].type == 'conditionlist':
            self.conditionlist_c(root, tree.children[0], sc, ident)

    def conditionvariable_c(self, tree):
        return tree.children[1]

    def conditionlist_c(self, root, tree, sc, ident):
        if not isinstance(tree.children[1], str):
            self.conditionlistparamlist_c(root, tree.children[1], sc, ident)

    def conditionlistparamlist_c(self, root, tree, sc, ident):
        for child in tree.children:
            if not isinstance(child, str):
                if child.type == 'conditionlistparamlist':
                    self.conditionlistparamlist_c(root, child, True, ident)
                elif child.type == 'conditionlistparam':
                    self.conditionlistparam_c(root, child, sc, ident)

    def conditionlistparam_c(self, root, tree, sc, ident):
        for child in tree.children:
            if not isinstance(child, str):
                if child.type == 'objectcondition':
                    self.objectcondition_c(root, child, sc)
            elif isinstance(child, str) and child != '"':
                if sc:
                    root.set_children(self.node('expression', '{} = {};'.format(ident, tree.children[1]), []))
                else:
                    root.set_children(self.node('expression', '{} = {}'.format(ident, tree.children[1]), []))

    def do_rules(self, tree):
        pdl = self.program_c(tree)
        return pdl
