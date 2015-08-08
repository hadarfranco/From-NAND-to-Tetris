
__author__ = 'francoland'

A_COMMAND = 1
C_COMMAND = 2
L_COMMAND = 3
EMPTY_LINE = ""
NULL = "null"
POP_INDEX = 0

class Parser:

    def __init__(self, input_name):
        self.f = open(input_name, "r")
        self.lines = self.f.readlines()
        self.next_line = EMPTY_LINE
        self.curr_type = 0

    def has_more_commands(self):
        while self.lines:
            self.next_line = self.lines.pop(POP_INDEX)
            self.next_line = ''.join(self.next_line.split())
            is_comment = self.next_line.startswith("//")

            # the current line is a comment or an empty line - continue to the next line in the file
            if (not is_comment) and (not self.next_line == "") and (not self.next_line == "\n"):
                if "//" in self.next_line:
                    index = self.next_line.index("//")
                    self.next_line = self.next_line[:index]
                return True
        return False

    def advance(self):
        return self.next_line

    def command_type(self):
        if self.next_line.startswith("@"):
            self.curr_type = A_COMMAND
            return A_COMMAND
        elif self.next_line.startswith("("):
            self.curr_type = L_COMMAND
            return L_COMMAND
        else:
            self.curr_type = C_COMMAND
            return C_COMMAND

    def symbol(self):
        if self.curr_type == A_COMMAND:
            return self.next_line[1:]
        if self.curr_type == C_COMMAND:
            return self.next_line[1:-1] # remove ()

    def dest(self):
        if self.curr_type == C_COMMAND:
            if "=" in self.next_line:
                index = self.next_line.index("=")
                return self.next_line[:index]
        return NULL

    def comp(self):
        if self.curr_type == C_COMMAND:
            if ("=" in self.next_line) and (";" in self.next_line):
                indexEquality = self.next_line.index("=")
                indexSeperator = self.next_line.index(";")
                return self.next_line[indexEquality + 1 : indexSeperator]
            if ";" in self.next_line:
                index = self.next_line.index(";")
                return self.next_line[:index]
            if "=" in self.next_line:
                index = self.next_line.index("=")
                return self.next_line[index + 1 :]
        return NULL


    def jump(self):
        if self.curr_type == C_COMMAND:
            if ";" in self.next_line:
                index = self.next_line.index(";")
                return self.next_line[index + 1 :]
        return NULL
