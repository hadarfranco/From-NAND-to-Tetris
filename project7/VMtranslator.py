__author__ = 'francoland'

from Parser import Parser
from CodeWriter import CodeWriter
from Parser import C_ARITHMETIC, C_POP, C_PUSH

import sys
from os import listdir
from os.path import isfile, isdir, join

FILE_POS = 1

def main():
    input_path = sys.argv[FILE_POS]
    if isdir(input_path):
        input_list = [ input_path + "/" +f for f in listdir(input_path)
            if (isfile(join(input_path, f))) and (f.endswith(".vm")) ]
        # check if we're getting a path or something else
        index = input_path.rfind("/")
        name = input_path[index + 1:]
        output_file_name = input_path + "/" + name + ".asm"
    else:
        input_list = [input_path]
        index = input_path.index(".vm")
        output_file_name = input_path[:index] + ".asm"

    code_writer = CodeWriter(output_file_name)

    for input_file in input_list:
        parser = Parser(input_file)
        code_writer.set_file_name(input_file)
        while parser.has_more_commands():
            command = parser.advance()
            if parser.command_type() == C_ARITHMETIC:
                code_writer.write_arithmetic(command)
            if (parser.command_type() == C_PUSH) or (parser.command_type() == C_POP):
                code_writer.write_push_pop(parser.command_type(), parser.arg1(), parser.arg2())

    code_writer.close()

if __name__ == "__main__":
    main()




