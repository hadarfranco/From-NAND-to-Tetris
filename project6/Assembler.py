__author__ = 'francoland'

from __builtin__ import bin
from Parser import Parser
from Parser import A_COMMAND, C_COMMAND, L_COMMAND, EMPTY_LINE
from Code import Code
from SymbolTable import SymbolTable

import sys

from os import listdir
from os.path import isfile, isdir, join

FILE_POS = 1
C_PREFIX_REG = "111"
C_PREFIX_SPE = "101"
A_PREFIX = "0"
FIRST_ADDRESS_RAM = 16
FIRST_ADDRESS_ROM = 0

def main():
    # open an output file
    input_path = sys.argv[FILE_POS]
    if isdir(input_path):
        input_list = [ input_path + "/" +f for f in listdir(input_path) 
            if (isfile(join(input_path, f))) and (f.endswith(".asm")) ]
    else:
        input_list = [input_path]
    
    for input_file in input_list:
        index = input_file.index(".")
        output_file = open(input_file[:index] + ".hack", "w")
        # parse a new line
        code = Code()
        symbol_table = SymbolTable()
        counter_address = FIRST_ADDRESS_RAM
        counter_rom = FIRST_ADDRESS_ROM

        # first pass
        parser_first_pass = Parser(input_file)
        while parser_first_pass.has_more_commands():
            command = parser_first_pass.advance()
            parse_type = parser_first_pass.command_type()
            if parse_type == L_COMMAND:
                if not symbol_table.contains(command[1:-1]):
                    symbol_table.add_entry(command[1:-1], counter_rom)
            else:
               counter_rom+=1

        # second pass
        parser_second_pass = Parser(input_file)
        while parser_second_pass.has_more_commands():
            command = parser_second_pass.advance()
            line_to_hack = ""
            parse_type = parser_second_pass.command_type()

            # translate the line to an A Command
            if parse_type == A_COMMAND:
                if command[1:].isdigit():
                    address = command[1:]
                else:
                    if symbol_table.contains(command[1:]):
                        address = symbol_table.get_address(command[1:])
                    else:
                        symbol_table.add_entry(command[1:], counter_address)
                        address = counter_address
                        
                        counter_address += 1
                binary_repr = str(bin(int(address))[2:].zfill(15))
                line_to_hack = A_PREFIX + binary_repr

            # translate the line to a C Command
            if parse_type == C_COMMAND:
                # C command comp
                comp_type = parser_second_pass.comp()
                code_comp = code.comp(comp_type)
                # C command dest
                dest_type = parser_second_pass.dest()
                code_dest = code.dest(dest_type)
                # C command jump
                jump_type = parser_second_pass.jump()
                code_jump = code.jump(jump_type)
                if ("<" in comp_type) or (">" in comp_type):
                    line_to_hack = C_PREFIX_SPE + code_comp + code_dest + code_jump
                else:
                    line_to_hack = C_PREFIX_REG + code_comp + code_dest + code_jump
                
            if parse_type == L_COMMAND:
                continue

            # write the line to the output file
            output_file.write(line_to_hack + "\n")


        output_file.close()


if __name__ == "__main__":
    main()
