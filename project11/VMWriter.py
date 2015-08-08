__author__ = 'francoland'

CONST = "constant"
LCL = "local"
STATIC = "static"
ARGUMENT = "argument"
THIS = "this"
THAT = "that"
POINTER = "pointer"
TEMP = "temp"


class VMWriter:

    def __init__(self, output_file):
        self.output = open(output_file, "w")

    def write_push(self, segment, index):
        # remember to send the segment as a string
        command = "push " + segment + " " + str(index) + "\n"
        self.output.write(command)

    def write_pop(self, segment, index):
        command = "pop " + segment + " " + str(index) + "\n"
        self.output.write(command)

    def write_arithmetic(self, command):
        # command should be a string
        self.output.write(command + "\n")

    def write_label(self, label):
        command = "label " + label + "\n"
        self.output.write(command)

    def write_go_to(self, label):
        command = "goto " + label + "\n"
        self.output.write(command)

    def write_if(self, label):
        command = "if-goto " + label + "\n"
        self.output.write(command)

    def write_call(self, name, n_args):
        command = "call " + name + " " + str(n_args) + "\n"
        self.output.write(command)

    def write_function(self, name, n_locals):
        command = "function " + name + " " + str(n_locals) + "\n"
        self.output.write(command)

    def write_return(self):
        self.output.write("return\n")

    def close(self):
        self.output.close()