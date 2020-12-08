from program.converter_pdl.converter import MyPdlConverter
from program.converter_nuxmv.converter import MyNuxmvConverter
from program.blockchain.smv_code_compiler import make_blockchain
import sys
from os import walk
from os.path import isfile


def print_help(path):
    help = open(path, "r")
    print(help.read())
    help.close()


def set_converter(path, option):
    filesNames = get_files(path)
    options = get_options()
    if option == '-c' or option == '-j':
        converter = MyPdlConverter(options)
        for filename in filesNames:
            file = open(filename, "r")
            converter.make_conversion(file)
            file.close()
    elif option == '-cn' or option == '-jn':
        converter = MyNuxmvConverter(options)
        for filename in filesNames:
            file = open(filename, "r")
            converter.make_conversion(file)
            file.close()


def set_block(path):
    filesNames = get_files(path)
    files = []
    for filename in filesNames:
        files.append(open(filename, "r"))
    options = get_options()
    make_blockchain(files, options)
    for file in files:
        file.close()


def set_option(options, option, index, reserved):
    if index+1 < len(sys.argv) and sys.argv[index+1] not in reserved:
        options[option] = sys.argv[index+1]
    else:
        print('WARNING: your {} is invalid.'.format(option))


def get_files(path):
    if len(sys.argv) > 2:
        arg = sys.argv[2]
        if isfile(path + arg):
            return [path + arg]
        else:
            files = []
            for (_, _, filenames) in walk(path + arg):
                for i in range(0, len(filenames)):
                    filenames[i] = path + arg + filenames[i]
                files.extend(filenames)
                break
            return files
    print("you have to pass a path to the files")
    return []


def get_options():
    reserved = ['-h', '-hc', '-hj', '-c', '-cn',
                '-j', '-jn', '-b', '-bc', '-bj',
                '-g', '-m', '-nodes', '-users',
                '-balance', '-transactions', '-block',
                '-int', '-integer', '-pdl',
                '-positive',  '-smv', '-32b', '-64b']
    options = {}

    for i in range(1, len(sys.argv)):
        option = sys.argv[i]

        if option in reserved:
            if option == '-int':
                if i+2 < len(sys.argv) and sys.argv[i+1].isnumeric() and sys.argv[i+2].isnumeric():
                    top = max(int(sys.argv[i+1]), int(sys.argv[i+2]))
                    bottom = min(int(sys.argv[i+1]), int(sys.argv[i+2]))
                    options['int'] = [bottom, top]
                else:
                    print('WARNING: your int must be a numeric value')

            elif option == '-b':
                options['program'] = 0

            elif option == '-c' or option == '-cn' or option == '-bc':
                options['program'] = 1

            elif option == '-j' or option == '-jn' or option == '-bj':
                options['program'] = 2

            elif option == '-integer':
                options['integer'] = True

            elif option == '-pdl':
                if i+1 < len(sys.argv) and sys.argv[i+1] not in reserved:
                    options['pdl'] = sys.argv[i+1]
                else:
                    print('WARNING: your pdl name must not be a reserved word.')

            elif option == '-positive':
                options['positive'] = True

            elif option == '-32b':
                options['32b'] = True

            elif option == '-64b':
                options['64b'] = True

            elif option == '-m':
                options['autogen'] = False
                if i+5 < len(sys.argv) and sys.argv[i+1].isnumeric() and sys.argv[i+2].isnumeric():
                    options['nodes_quantity'] = int(sys.argv[i+1])
                    options['users_quantity'] = int(sys.argv[i+2])
                    path = './options/'
                    if isfile(path + sys.argv[i+3]) and isfile(path + sys.argv[i+4]) and isfile(sys.argv[i+5]):
                        options['balance_file'] = open(
                            path + sys.argv[i+3], "r")
                        options['transactions_file'] = open(
                            path + sys.argv[i+4], "r")
                        options['block_file'] = open(path + sys.argv[i+5], "r")
                else:
                    print('WARNING: you must pass valid parameters.')
            elif option == '-g':
                options['autogen'] = True
                set_option(options, 'seeds', i, reserved)
            elif option == '-smv':
                set_option(options, 'smv', i, reserved)
            elif option == '-nodes':
                set_option(options, 'nodes', i, reserved)
            elif option == '-users':
                set_option(options, 'users', i, reserved)
            elif option == '-balance':
                set_option(options, 'balance', i, reserved)
            elif option == '-transactions':
                set_option(options, 'transactions', i, reserved)
            elif option == '-block':
                set_option(options, 'block', i, reserved)
    return options


if len(sys.argv) > 1:
    type = sys.argv[1]
    if type == '-h':
        print_help("help")
    elif type == '-hb':
        print_help("./program/blockchain/help")
    elif type == '-hc':
        print_help("./program/converter_pdl/rules_c/help")
    elif type == '-hj':
        print_help("./program/converter_pdl/rules_smacco/help")
    elif type == '-c' or type == '-cn':
        set_converter("./samples/sample_c/", type)
    elif type == '-j' or type == '-jn':
        set_converter("./samples/sample_smacco/", type)
    elif type == '-b':
        options = get_options()
        make_blockchain(None, options)
    elif type == '-bc':
        set_block("./samples/sample_c/")
    elif type == '-bj':
        set_block("./samples/sample_smacco/")
else:
    print("you have to pass a routine parameter")
