from src.pdl.converter import MyPdlConverter
from src.nuxmv.converter import MyNuxmvConverter
import sys
from os import walk
from os.path import isfile


def set_converter(path, option):
    filesNames = get_files(path)
    options = get_options()
    converter = MyNuxmvConverter(options)

    for filename in filesNames:
        with open(filename, "r") as code:
            converter.make_conversion(code)


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
    reserved = ['-cn', '-smv']
    options = {}
    for i in range(1, len(sys.argv)):
        option = sys.argv[i]
        if option in reserved:
            if option == '-c' or option == '-cn' or option == '-bc':
                options['program'] = 1
            elif option == '-smv':
                set_option(options, 'smv', i, reserved)

    return options


if __name__ == '__main__':
    #python3 verifier.py -cn assignc.c -smv outfile  
    if len(sys.argv) > 1 and sys.argv[1] == "help":
        print("HELP")
    else:
        set_converter("./examples/", '-cn')
