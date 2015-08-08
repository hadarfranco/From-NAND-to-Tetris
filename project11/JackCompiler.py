__author__ = 'francoland'


from CompilationEngine import  CompilationEngine

import sys
from os import listdir
from os.path import isfile, isdir, join


FILE_POS = 1

def main():
    input_path = sys.argv[FILE_POS]
    if isdir(input_path):
        input_list = [ input_path + "/" +f for f in listdir(input_path)
            if (isfile(join(input_path, f))) and (f.endswith(".jack")) ]
        for f in input_list:
            index = f.rfind(".jack")
            output_file_name = f[:index] + ".vm"
            compiler = CompilationEngine(f, output_file_name)
            compiler.compile_class()
    else:
        index = input_path.find(".jack")
        output_file_name = input_path[:index] + ".vm"
        compiler = CompilationEngine(input_path, output_file_name)
        compiler.compile_class()


if __name__ == "__main__":
    main()
