from operator import __eq__

__author__ = 'francoland'

EMPTY_LINE = ""
from Parser import C_ARITHMETIC, C_PUSH, C_POP

CONST = "constant"
LCL = "local"
ARG = "argument"
THIS = "this"
THAT = "that"
ADD = "add"
SUB = "sub"
NEG = "neg"
EQ = "eq"
GT = "gt"
LT = "lt"
AND = "and"
OR = "or"
NOT = "not"

PUSH_POINTER_TEMP = "D = D + A\n" \
                    "A = D\n" \
                    "D = M\n" \
                    "@SP\n" \
                    "A = M\n" \
                    "M = D\n"

POP_TEMP = "D = D + A\n" \
           "@R13\n" \
           "M = D\n" \
           "@SP\n" \
           "M = M - 1\n" \
           "A = M\n" \
           "D = M\n" \
           "@R13\n" \
           "A = M\n" \
           "M = D\n"

BIN_OPER_FIRST = "D = M\n" \
                 "@R13\n" \
                 "M = D\n" \
                 "@SP\n" \
                 "D = M\n" \
                 "D = D - 1\n" \
                 "M = D\n" \
                 "A = M\n" \
                 "D = M\n" \
                 "@R13\n"

COMPARE_START = "D = M\n" \
            	"@R13\n" \
	            "M = D\n" \
            	"@SP\n" \
            	"D = M\n" \
                "D = D - 1\n" \
            	"M = D\n" \
	            "A = M\n" \
            	"D = M\n" \
            	"@R14\n" \
                "M=D\n"

BIN_OPER_SECOND = "@SP\n" \
                  "A = M\n" \
                  "M = D\n"

SP_HEAD = "@SP\n" \
          "M = M - 1\n" \
          "A = M\n"

SP_INC = "@SP\n" \
         "M = M + 1\n"

NEG_OPER = "D = -M\n" \
           "M = D\n"

ADD_OPER = "D = D + M\n"

SUB_OPER = "D = D - M\n"

AND_OPER = "D = D&M\n"

OR_OPER = "D = D|M\n"

NOT_OPER = "D = !M\n" \
           "M = D\n"

PUSH_OPER = "D = A\n" \
            "@SP\n" \
            "A = M\n" \
            "M = D\n"

CALL_OPER = "D = M\n" \
            "@SP\n" \
            "A = M\n" \
            "M = D\n"

class CodeWriter:

    def __init__(self, output):
        self.output_file = open(output, "w")
        self.file_name = ""
        self.counter_loop = 1
        self.counter_return = 1
        self.mem_segments = {LCL : "LCL", ARG : "ARG", THIS : "THIS", THAT : "THAT"}
        self.curr_function_name = ""
        self.curr_num_locals = 0

    def set_file_name(self, file_name):
        index = file_name.find(".vm")
        self.file_name = file_name[:index]
        if "/" in self.file_name:
            index = self.file_name.rfind("/")
            self.file_name = self.file_name[index+1:]


    def write_arithmetic(self, command):
        temp_line = ""
        if command == ADD:
            temp_line = SP_HEAD + BIN_OPER_FIRST + ADD_OPER + BIN_OPER_SECOND + SP_INC
        if command == SUB:
            temp_line = SP_HEAD + BIN_OPER_FIRST + SUB_OPER + BIN_OPER_SECOND + SP_INC
        if command == NEG:
            temp_line = SP_HEAD + NEG_OPER + SP_INC
        if command == EQ:
            temp_line = SP_HEAD + COMPARE_START + self.compare_eq() + self.compare_oper() + SP_INC
            self.counter_loop+=1
        if command == GT:
            temp_line = SP_HEAD + COMPARE_START + self.compare_gt() + self.compare_oper() + SP_INC
            self.counter_loop+=1
        if command == LT:
            temp_line = SP_HEAD + COMPARE_START + self.compare_lt() + self.compare_oper() + SP_INC
            self.counter_loop+=1
        if command == AND:
            temp_line = SP_HEAD + BIN_OPER_FIRST + AND_OPER + BIN_OPER_SECOND + SP_INC
        if command == OR:
            temp_line = SP_HEAD + BIN_OPER_FIRST + OR_OPER + BIN_OPER_SECOND + SP_INC
        if command == NOT:
            temp_line = SP_HEAD + NOT_OPER + SP_INC
        self.output_file.write(temp_line)

    def write_push_pop(self, command, segment, index):
        temp_line = ""
        if command == C_PUSH:
            if segment == CONST:
                temp_line = "@" + str(index) + "\n" + PUSH_OPER + SP_INC
            elif segment in self.mem_segments:
                temp_line = "@" + self.mem_segments[segment] + "\n" \
                            "D = M\n" \
                            "@" + str(index) + "\n" \
                            "D = D + A\n" \
                            "A = D\n" \
                            "D = M\n" \
                            "@SP\n" \
                            "A = M\n" \
                            "M = D\n" \
                            + SP_INC
            elif segment == "pointer":
                temp_line = "@R3\n" \
                            "D = A\n" \
                            "@" + str(index) + "\n" \
                            + PUSH_POINTER_TEMP \
                            + SP_INC
            elif segment == "temp":
                    temp_line = "@R5\n" \
                                "D = A\n" \
                                "@" + str(index) + "\n" \
                                + PUSH_POINTER_TEMP \
                                + SP_INC
            elif segment == "static":
                    temp_line = "@" + self.file_name + "." + str(index) + "\n" \
                                "D = M\n" \
                                "@SP\n" \
                                "A = M\n" \
                                "M = D\n" \
                                + SP_INC
        if command == C_POP:
            if segment in self.mem_segments:
                temp_line = SP_HEAD + \
                            "D = M\n" \
                            "@13\n" \
                            "M = D\n" \
                            "@" + self.mem_segments[segment] +"\n" \
                            "D = M\n" \
                            "@" + str(index) + "\n" \
                            "D = D + A\n" \
                            "@R14\n" \
                            "M = D\n" \
                            "@13\n" \
                            "D = M\n" \
                            "@14\n" \
                            "A = M\n" \
                            "M = D\n"
            elif segment == "pointer":
                if index == 0:
                    temp_line = SP_HEAD + \
                                "D = M\n" \
                                "@R3\n" \
                                "M = D\n"
                else:
                    temp_line = SP_HEAD + \
                                "D = M\n" \
                                "@R4\n" \
                                "M = D\n"
            elif segment == "temp":
                temp_line = "@R5\n" \
                            "D = A\n" \
                            "@" + str(index) + "\n" \
                            + POP_TEMP
            elif segment == "static":
                temp_line = SP_HEAD + \
                            "D = M\n" \
                            "@" + self.file_name + "." + str(index) + "\n" \
                            "M = D\n"
        self.output_file.write(temp_line)

    def write_init(self):
        temp_line = "@256\n" \
                    "D = A\n" \
                    "@SP\n" \
                    "M = D\n"
        self.output_file.write(temp_line)
        self.curr_function_name = "Sys.init"
        self.write_call(self.curr_function_name, 0)


    def write_label(self, label):
        temp_line = "(" + self.curr_function_name + ":" + label + ")\n"
        self.output_file.write(temp_line)

    def write_goto(self, label):
        temp_line = "@" + self.curr_function_name + ":" + label + "\n" \
                    "0;JMP\n"
        self.output_file.write(temp_line)

    def write_if(self, label):
        temp_line = SP_HEAD + \
                    "D = M\n" \
                    "@" + self.curr_function_name + ":" + label + "\n" \
                    "D;JNE\n"
        self.output_file.write(temp_line)

    def write_call(self, function_name, num_args):
        self.write_push_pop(C_PUSH, CONST, "RETURN" + str(self.counter_return))
        temp_line = "@LCL\n" \
                    + CALL_OPER \
                    + SP_INC
        temp_line += "@ARG\n" \
                    + CALL_OPER \
                    + SP_INC
        temp_line += "@THIS\n" \
                    + CALL_OPER \
                    + SP_INC
        temp_line += "@THAT\n" \
                    + CALL_OPER \
                    + SP_INC
        # ARG = SP - n - 5
        temp_line += "@SP\n" \
                     "D = M\n" \
                     "@ARG\n" \
                     "M = D\n" \
                     "@" + str(num_args) + "\n" \
                     "D = A\n" \
                     "@ARG\n" \
                     "M = M - D\n" \
                     "@5\n" \
                     "D = A\n" \
                     "@ARG\n" \
                     "M = M - D\n"
        # LCL = SP
        temp_line += "@SP\n" \
                     "D = M\n" \
                     "@LCL\n" \
                     "M = D\n"
        #goto f
        temp_line += "@" + function_name + "\n" \
                     "0;JMP\n"
        temp_line +=  "(RETURN" + str(self.counter_return) + ")\n"
        self.output_file.write(temp_line)
        self.counter_return+=1

    def write_return(self):
        # FRAME = LCL
        temp_line = "@LCL\n" \
                    "D = M\n" \
                    "@FRAME\n" \
                    "M = D\n"
        # RET = *(FRAME - 5)
        temp_line += "@5\n" \
                     "D = A\n" \
                     "@FRAME\n" \
                     "D = M - D\n" \
                     "A = D\n" \
                     "D = M\n" \
                     "@RET\n" \
                     "M = D\n"
        # *ARG = pop()
        temp_line += SP_HEAD +\
                    "D = M\n" \
                    "@ARG\n" \
                    "A = M\n" \
                    "M = D\n"
        # SP = ARG + 1
        temp_line += "@ARG\n" \
                     "D = M + 1\n" \
                     "@SP\n" \
                     "M = D\n"
        # THAT = *(FRAME-1)
        temp_line += "@FRAME\n" \
                     "D = M - 1\n" \
                     "@R13\n" \
                     "M = D\n" \
                     "A = D\n" \
                     "D = M\n" \
                     "@THAT\n" \
                     "M = D\n"
        # THIS = *(FRAME - 2)
        temp_line += "@R13\n" \
                     "M = M - 1\n" \
                     "A = M\n" \
                     "D = M\n" \
                     "@THIS\n" \
                     "M = D\n"
        # ARG = *(FRAME - 3)
        temp_line += "@R13\n" \
                     "M = M - 1\n" \
                     "A = M\n" \
                     "D = M\n" \
                     "@ARG\n" \
                     "M = D\n"
        # LCL = *(FRAME - 4)
        temp_line += "@R13\n" \
                     "M = M - 1\n" \
                     "A = M\n" \
                     "D = M\n" \
                     "@LCL\n" \
                     "M = D\n"
        # goto RET
        temp_line += "@RET\n" \
                    "A = M\n" \
                    "0;JMP\n"
        self.output_file.write(temp_line)

    def write_function(self, function_name, num_locals):
        if function_name == "Sys.init":
            temp_line = "(" + function_name + ")\n"
        else:
            temp_line = "(" + str(function_name) + ")\n"
        self.curr_function_name = str(function_name)
        self.output_file.write(temp_line)
        for i in range(1, num_locals + 1):
            self.write_push_pop(C_PUSH, CONST, 0)

    def close(self):
       self.output_file.close()

    def compare_oper(self):
        return "@SP\n" \
               "A = M\n" \
               "M = 0\n" \
               "@END" + str(self.counter_loop) + "\n" \
               "0;JMP\n" \
               "(LOOP" + str(self.counter_loop) + ")\n" \
               "@SP\n" \
               "A = M\n" \
               "M = -1\n" \
               "(END" + str(self.counter_loop) + ")\n"

    def compare_eq(self):
        return "@POSITIVE" + str(self.counter_loop) + "\n" \
               "D,JGT\n" \
               "@R13\n" \
               "D=M\n" \
               "@COMPARE" + str(self.counter_loop) + "\n" \
               "D,JLE\n" \
               "@SP\n" \
               "A = M\n" \
               "M = 0\n" \
               "@END" + str(self.counter_loop) + "\n" \
               "0;JMP\n" \
               "(POSITIVE" + str(self.counter_loop) + ")\n" \
               "@R13\n" \
               "D=M\n" \
               "@COMPARE" + str(self.counter_loop) + "\n" \
               "D,JGT\n" \
               "@SP\n" \
               "A = M\n" \
               "M = 0\n" \
               "@END" + str(self.counter_loop) + "\n" \
               "0;JMP\n" \
               "(COMPARE" + str(self.counter_loop) + ")\n" \
               "@R14\n" \
               "D=M\n" \
               "@R13\n" \
               "D = D - M\n" \
               "@LOOP" + str(self.counter_loop) + "\n" \
               "D;JEQ\n"

    def compare_gt(self):
        return "@POSITIVE" + str(self.counter_loop) + "\n" \
               "D,JGT\n" \
               "@R13\n" \
               "D=M\n" \
               "@COMPARE" + str(self.counter_loop) + "\n" \
               "D,JLE\n" \
               "@SP\n" \
               "A = M\n" \
               "M = 0\n" \
               "@END" + str(self.counter_loop) + "\n" \
               "0;JMP\n" \
               "(POSITIVE" + str(self.counter_loop) + ")\n" \
               "@R13\n" \
               "D=M\n" \
               "@COMPARE" + str(self.counter_loop) + "\n" \
               "D,JGT\n" \
               "@SP\n" \
               "A = M\n" \
               "M = -1\n" \
               "@END" + str(self.counter_loop) + "\n" \
               "0;JMP\n" \
               "(COMPARE" + str(self.counter_loop) + ")\n" \
               "@R14\n" \
               "D=M\n" \
               "@R13\n" \
               "D = D - M\n" \
               "@LOOP" + str(self.counter_loop) + "\n" \
               "D;JGT\n"

    def compare_lt(self):
        return "@POSITIVE" + str(self.counter_loop) + "\n" \
               "D,JGT\n" \
               "@R13\n" \
               "D=M\n" \
               "@COMPARE" + str(self.counter_loop) + "\n" \
               "D,JLE\n" \
               "@SP\n" \
               "A = M\n" \
               "M = -1\n" \
               "@END" + str(self.counter_loop) + "\n" \
               "0;JMP\n" \
               "(POSITIVE" + str(self.counter_loop) + ")\n" \
               "@R13\n" \
               "D=M\n" \
               "@COMPARE" + str(self.counter_loop) + "\n" \
               "D,JGT\n" \
               "@SP\n" \
               "A = M\n" \
               "M = 0\n" \
               "@END" + str(self.counter_loop) + "\n" \
               "0;JMP\n" \
               "(COMPARE" + str(self.counter_loop) + ")\n" \
               "@R14\n" \
               "D=M\n" \
               "@R13\n" \
               "D = D - M\n" \
               "@LOOP" + str(self.counter_loop) + "\n" \
               "D;JLT\n"