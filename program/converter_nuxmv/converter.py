import os
from program.converter_pdl.converter import MyPdlConverter


class MyNuxmvConverter:

    def __init__(self, options):
        self.options = options
        self.base_func = False
        self.name = ''
        self.reserved = ['(', 'U', 'U~', ')', ')*', ');',
                         ')?', ')?;', '=', '==', '!=', '>',
                         '<', '>=', '<=', ';']
        self.variable_list = []
        self.nuxmv = ''

    def program(self, tree, file):
        if tree != None:
            for child in tree.children:
                self.module(child, file)

    def module(self, tree, file):
        type = tree.type.split(' ')
        if len(type) > 1:
            if self.base_func and type[1] == 'main':
                file.write('MODULE {}_{}\n'.format(self.name, type[1]))
                self.nuxmv += 'MODULE {}_{}_{}\n'.format(self.name, self.name, type[1])
            else:
                file.write('MODULE {}\n'.format(type[1]))
                self.nuxmv += 'MODULE {}_{}\n'.format(self.name, type[1])
        else:
            self.base_func = True
            file.write('MODULE main\n')
            self.nuxmv += 'MODULE {}_main\n'.format(self.name)
        self.var(tree, file)

    def var(self, tree, file):
        file.write('\nVAR\n\tprogram : {')
        self.nuxmv += '\nVAR\n\tprogram : {'
        self.var_item(tree, file, 0)
        self.variable_list = []
        file.write('};\n\t')
        self.nuxmv += '};\n\t'
        self.variable(tree)
        pos = 0
        for item in self.variable_list:
            self.search_variable(tree, item, 0, pos)
            pos += 1
        self.variable_list = [i for i in self.variable_list if len(i) > 1]
        self.set_variable(tree, file)
        self.assign(tree, file)

    def var_item(self, tree, file, pos):
        for child in tree.children:
            if child.value not in self.reserved:
                if pos > 0:
                    item = ', {}_{}'.format(child.value.replace(
                        ' ', '_').replace(';', ''), pos)
                else:
                    item = '{}_{}'.format(child.value.replace(
                        ' ', '_').replace(';', ''), pos)
                if self.base_func:
                    item = item.replace('main', '{}_main'.format(self.name))
                item = item.replace('{', '(').replace('}', ')')
                file.write(item)
                self.nuxmv += item.replace('main', '{}_main'.format(self.name))
                pos += 1
            else:
                pos = self.var_item(child, file, pos)
        return pos

    def variable(self, tree):
        for child in tree.children:
            if child.value not in self.reserved and '{' not in child.value and '}' not in child.value:
                value = child.value.split(' ')
                for item in value:
                    if item != 'int' and item != 'float' and item not in self.reserved:
                        present = False
                        for elem in self.variable_list:
                            if item in elem:
                                present = True
                        if not present:
                            self.variable_list.append([item.replace(';','')])
                    elif item in self.reserved:
                        break
            else:
                self.variable(child)

    def search_variable(self, tree, item, pos, listpos):
        for child in tree.children:
            if item[0] in child.value and '=' in child.value and child.value not in self.reserved:
                if child.value.index(item[0]) < child.value.index('='):
                    self.variable_list[listpos].append('{}_{}'.format(child.value, pos).replace(' ', '_').replace(';', ''))
            elif child.value not in self.reserved:
                pos += 1
            else:
                pos = self.search_variable(child, item, pos, listpos)
        return pos

    def set_variable(self, tree, file):
        variable_list = []
        for item in self.variable_list:
            minimum = ''
            maximum = ''
            number = False
            for pos in range(1, len(item)):
                prog = item[pos].split('_')
                if '=' in prog and '==' not in prog:
                    index = prog.index('=')
                    if prog[index + 1].isnumeric():
                        if not minimum.isnumeric() and not maximum.isnumeric():
                            minimum = prog[index+1]
                            maximum = prog[index+1]
                        else:
                            minimum = min(minimum, prog[index+1])
                            maximum = max(maximum, prog[index+1])
                        number = True
            if number:
                if isinstance(minimum, str) and isinstance(maximum, str):
                    file.write('{} : {}..{};\n\t'.format(item[0], minimum, maximum))
                    self.nuxmv += '{} : {}..{};\n\t'.format(item[0], minimum, maximum)
                else:
                    file.write('{} : {}..{};\n\t'.format(item[0], 0, 0))
                    self.nuxmv += '{} : {}..{};\n\t'.format(item[0], 0, 0)
                variable_list.append(item)
        self.variable_list = variable_list

    def assign(self, tree, file):
        file.write('\nASSIGN\n\tinit(progam) := ')
        self.nuxmv += '\nASSIGN\n\tinit(progam) := '
        if tree.children[0].value != '(':
            file.write('{}_0;\n\t'.format(tree.children[0].value.replace(';', '').replace(' ', '_')))
            self.nuxmv += '{}_0;\n\t'.format(tree.children[0].value.replace(';', '').replace(' ', '_'))
        else:
            file.write('{')
            self.nuxmv += '{'
            last = False
            for child in tree.children[0].children:
                if 'open' in child.type:
                    if last:
                        file.write(', {}'.format(child.children[0].value.replace(';', '').replace(' ', '_')))
                        self.nuxmv += ', {}'.format(child.children[0].value.replace(';', '').replace(' ', '_'))
                    else:
                        last = True
                        file.write('{}'.format(child.children[0].value.replace(';', '').replace(' ', '_')))
                        self.nuxmv += '{}'.format(child.children[0].value.replace(';', '').replace(' ', '_'))
            file.write('};\n\t')
            self.nuxmv += '};\n\t'
        for item in self.variable_list:
            element = item[1].split('_')
            index = element.index('=')
            file.write('init({}) := {};\n\t'.format(item[0], element[index+1]))
            self.nuxmv += 'init({}) := {};\n\t'.format(item[0], element[index+1])
        self.next(tree, file)

    def next(self, tree, file):
        file.write('next(prog) := case\n\t\t\t')
        self.nuxmv += 'next(prog) := case\n\t\t\t'
        program_list = self.next_program(tree, file, 0, '')
        self.set_next(program_list, file)
        for item in self.variable_list:
            self.next_variables(item, file)
        file.write('\n\n')
        self.nuxmv += '\n\n'

    def next_program(self, tree, file, pos, type):
        next_var = []
        for child in tree.children:
            if child.value not in self.reserved:
                item = child.value.replace(';', '').replace(' ', '_')
                if self.base_func:
                    item = item.replace('main', '{}_main'.format(self.name))
                if '?' in item:
                    item = [item, pos, type]
                next_var.append(item)
            elif len(child.children) > 0:
                arr = self.next_program(child, file, pos+1, child.type)
                for item in arr:
                    next_var.append(item)
        return next_var

    def set_next(self, item, file):
        for pos in range(0, len(item)):
            if pos < len(item)-1 and isinstance(item[pos], str) and isinstance(item[pos+1], str):
                file.write('prog = {}_{}: {}_{};\n\t\t\t'.format(item[pos], pos, item[pos+1].replace('{', '(').replace('}', ')'), pos+1))
                self.nuxmv += 'prog = {}_{}: {}_{};\n\t\t\t'.format(item[pos], pos, item[pos+1].replace('{', '(').replace('}', ')'), pos+1)
            elif pos < len(item)-1:
                first = item[pos]
                last = item[pos+1]
                if isinstance(item[pos], list):
                    first = item[pos][0]
                elif isinstance(item[pos+1], list):
                    if 'open_while_condition_neg' in item[pos+1][2]:
                        last = '{'
                        for pos_aux in reversed(range(0, pos)):
                            if isinstance(item[pos_aux], list) and item[pos+1][1] == item[pos_aux][1]:
                                last += '{}_{}'.format(item[pos_aux][0], pos_aux)
                                break
                        last += ', {}_{}'.format(item[pos+1][0], pos+1)
                        last += '}'
                    elif '_neg' in item[pos+1][2]:
                        last = '{}_{}'.format(item[pos][0], pos)
                    else:
                        last = '{'
                        last += '{}_{}'.format(item[pos+1][0], pos+1)
                        for pos_aux in range(pos+2, len(item)):
                            if isinstance(item[pos_aux], list) and item[pos+1][1] == item[pos_aux][1]:
                                last += ', {}_{}'.format(item[pos_aux][0], pos_aux)
                                break
                        last += '}'
                file.write('prog = {}_{}: {};\n\t\t\t'.format(first, pos, last))
                self.nuxmv += 'prog = {}_{}: {};\n\t\t\t'.format(first, pos, last)
        file.write('esac;\n\t')
        self.nuxmv += 'esac;\n\t'

    def next_variables(self, item, file):
        file.write('next({}) := case\n\t\t\t'.format(item[0]))
        self.nuxmv += 'next({}) := case\n\t\t\t'.format(item[0])
        for pos in range(1, len(item)):
            value = item[pos].split('_')[-1]
            file.write('prog = {} : {};\n\t\t\t'.format(item[pos], value))
            self.nuxmv += 'prog = {} : {};\n\t\t\t'.format(item[pos], value)
        file.write('TRUE = {};\n\t\t\tesac;\n'.format(item[0]))
        self.nuxmv += 'TRUE = {};\n\t\t\tesac;\n'.format(item[0])

    def make_conversion(self, file):
        if 'pdl' in self.options:
            self.name = self.options['pdl']
        else:
            self.name = os.path.basename(file.name).rsplit('.', 1)[0]
        converter = MyPdlConverter(self.options)
        tree = converter.make_conversion(file)
        if self.options['program'] == 1:
            out = open("./results/minic/{}.smv".format(self.name), "w")
        else:
            out = open("./results/smacco/{}.smv".format(self.name), "w")
        self.program(tree, out)
        out.close()
        return self.nuxmv
