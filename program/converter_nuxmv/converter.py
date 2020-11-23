import os
from program.converter_pdl.converter import MyPdlConverter


class MyNuxmvConverter:

    def __init__(self, options):
        self.options = options
        self.reserved = ['(', 'U', 'U~', ')', ')*', ');',
                         ')?', ')?;', '=', '==', '!=', '>',
                         '<', '>=', '<=']
        self.nuxmv = ''
        self.name = ''
        self.func_list = []
        self.nux_list = []
        self.main_variables = []
        self.pos = 0

    def program(self, tree, file):
        if tree != None:
            for child in tree.children:
                func_list, nux_list = self.func(child, [], [])
                self.func_list.append(func_list)
                self.nux_list.append(nux_list)
            for pos in range(len(tree.children)):
                self.module(tree.children[pos], file, pos)

    def module(self, tree, file, pos):
        self.nuxmv += 'Module {}\n\n\tVAR\n\t\tprogram: {{'.format(self.nux_list[pos][0])
        file.write('Module {}\n\n\tVAR\n\t\tprogram: {{'.format(self.func_list[pos][0]))

        for i in range(1, len(self.func_list[pos])):
            if i < len(self.func_list[pos])-1:
                self.nuxmv += '{};'.format(self.func_list[pos][i])
                file.write('{};'.format(self.func_list[pos][i]))
            else:
                self.nuxmv += '{}'.format(self.func_list[pos][i])
                file.write('{}'.format(self.func_list[pos][i]))

        self.nuxmv += '}\n\t\t'
        file.write('}\n\t\t')

        variables = []
        for expr in self.func_list[pos]:
            if 'int' in expr or 'float' in expr:
                max = 0
                min = 0
                ident = expr.split('_')[1]
                if pos == 0:
                    for lst in self.func_list:
                        for aux in lst:
                            if '{}_='.format(ident) in aux:
                                num = aux.replace('_', '=').split('=')[-2]
                                if num.isnumeric():
                                    num = float(num)
                                    if num > max:
                                        max = num
                                    elif num < min:
                                        min = num
                    self.main_variables.append(ident)
                    variables.append(ident)
                else:
                    for aux in self.func_list[pos]:
                        if '{}_= '.format(ident) in aux:
                                num = aux.replace('_', '=').split('=')[-2]
                                if num.isnumeric():
                                    num = float(num)
                                    if num > max:
                                        max = num
                                    elif num < min:
                                        min = num
                    variables.append(ident)
                self.nuxmv += '{}: {}...{}\n\t\t'.format(ident, min, max)
                file.write('{}: {}...{}\n\t\t'.format(ident, min, max))
        
        self.nuxmv += '\n\tASSIGN\n\t\tinit(prog):= '
        file.write('\n\tASSIGN\n\t\tinit(prog):= ')
        
        init = tree.children[0]
        if len(init.children) > 0:
            init_arr = []
            for child in init.children:
                if 'cond' in child.type:
                    init_arr.append(child.children[0].value).replace(';', '').replace(' ', '_')
        else:
            self.nuxmv += '{};'.format(init.value.replace(';', '').replace(' ', '_'))
            file.write('{};'.format(init.value.replace(';', '').replace(' ', '_')))
        
        if pos != 0:
            variables = variables + self.main_variables

        self.nuxmv += '\n\t\t'
        file.write('\n\t\t')
        for var in variables:
            assign = ''
            for expr in self.func_list[pos]:
                if '{}_='.format(var) in expr:
                    assign = expr.replace(';', '').split('=')[-1]
                    break
            if assign != '':
                self.nuxmv += 'init({}):= {};'.format(var, assign.split('_')[1])
                file.write('init({}):= {};'.format(var, assign.split('_')[1]))
                self.nuxmv += '\n\t\t'
                file.write('\n\t\t')

        self.nuxmv += 'next(program):= case\n\t\t\t'
        file.write('next(program):= case\n\t\t\t')
        for i in range(1, len(self.func_list[pos])-2):
            if '?' not in self.func_list[pos][i+1]:
                self.nuxmv += 'program = {} : {};\n\t\t\t'.format(self.func_list[pos][i], self.func_list[pos][i+1])
                file.write('program = {} : {};\n\t\t\t'.format(self.func_list[pos][i], self.func_list[pos][i+1]))
    
    def cond(self, tree):
        conds = []
        for pos in range(len(tree.children)):
            if 'open_cond' in tree.children[pos+1]:
                conds.append(tree.children[pos+1])
        return conds
    
    def func(self, tree, func_list, nux_list):
        self.pos = 0
        if tree.type == 'open_function':
            func_list.append('main')
            nux_list.append('{}_main'.format(self.name))
        else:
            func_list.append(tree.type.split(' ')[1].replace('main', 'main_func'))
            nux_list.append('{}_{}'.format(self.name, tree.type.split(' ')[1].replace('main', 'main_func')))
        for child in tree.children:
            self.expr(child, func_list, nux_list, self.pos)
            self.pos += 1
        return func_list, nux_list

    def expr(self, tree, f_list, nux_list, pos):
        if tree.type == 'expression':
            f_list.append('{}_{}'.format(tree.value.replace(';', '').replace(' ', '_'), pos))
            nux_list.append('{}_{}'.format(tree.value.replace(';', '').replace(' ', '_'), pos))
        elif tree.type == 'function':
            f_list.append(tree.value, pos)
            nux_list.append('{}_{}'.format(self.name, tree.value.replace(';', '').replace(' ', '_')))
        elif tree.type == 'function main':
            f_list.append('main_func')
            nux_list.append('{}_main_func'.format(self.name))
        else:
            for child in tree.children:
                self.expr(child, f_list, nux_list, pos)
                self.pos += 1

    def make_conversion(self, file):
        if 'pdl' in self.options:
            self.name = self.options['pdl']
        else:
            self.name = os.path.basename(file.name).rsplit('.', 1)[0]
        converter = MyPdlConverter(self.options)
        tree = converter.make_conversion(file)
        out = open("./results/{}.smv".format(self.name), "w")
        self.program(tree, out)
        out.close()
        return self.module
