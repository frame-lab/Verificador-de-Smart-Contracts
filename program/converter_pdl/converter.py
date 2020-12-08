from program.compiler.yacc import MyCompiler
from program.converter_pdl.rules_c.rules import MyCRules
from program.converter_pdl.rules_smacco.rules import MySmaccoRules
import os


class Node:
    def __init__(self, type, value, children):
        self.type = type
        self.value = value
        self.children = children

    def set_value(self, value):
        self.value = value

    def set_children(self, children):
        self.children.append(children)

    def __str__(self):
        if self.type.split(' ')[0] == 'open_function':
            if len(self.type.split(' ')) > 1:
                return "{} = {}".format(self.type.split(' ')[1], self.value)
            else:
                return "{}".format(self.value)
        elif self.type == 'end_function':
            return "{}\n".format(self.value)
        elif self.value == None:
            return ''
        else:
            return "{}".format(self.value)


class MyPdlConverter:
    def __init__(self, options):
        self.options = options

    def write_file(self, out, node):
        out.write(node.__str__())
        if node != None:
            for child in node.children:
                if isinstance(child, Node):
                    self.write_file(out, child)

    def make_conversion(self, file):
        if 'pdl' in self.options:
            name = self.options['pdl']
        else:
            name = os.path.basename(file.name).rsplit('.', 1)[0]
        data = str(file.read())
        compiler = MyCompiler(self.options, name)
        tree = compiler.make_parser(data)
        if self.options['program'] == 1:
            out = open("./results/minic/{}_pdl".format(name), "w")
        else:
            out = open("./results/smacco/{}_pdl".format(name), "w")
        pdl = None
        if tree != None:
            if self.options['program'] == 1:
                rules = MyCRules(Node)
                pdl = rules.do_rules(tree)
            elif self.options['program'] == 2:
                rules = MySmaccoRules(Node)
                pdl = rules.do_rules(tree)
            self.write_file(out, pdl)
        out.close()
        return pdl
