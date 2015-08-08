__author__ = 'francoland'

EMPTY_LINE = ""
POP_INDEX = 0
C_ARITHMETIC = 1
C_POP = 2
C_PUSH = 3
C_LABEL = 4
C_GOTO = 5
C_IF = 6
C_FUNCTION = 7
C_RETURN = 8
C_CALL = 9

class Parser:

    def __init__(self, input_name):
        self.f = open(input_name, "r")
        self.lines = self.f.readlines()
        self.next_line = EMPTY_LINE
        self.curr_type = 0
        self.commands_table = {"add" : C_ARITHMETIC, "sub" : C_ARITHMETIC, "neg" : C_ARITHMETIC, "eq" : C_ARITHMETIC,
                                "gt" : C_ARITHMETIC, "lt" : C_ARITHMETIC, "and" : C_ARITHMETIC, "or" : C_ARITHMETIC,
                                "not" : C_ARITHMETIC, "pop" : C_POP, "push" : C_PUSH, "label" : C_LABEL, "if" : C_IF,
                                "goto" : C_GOTO, "function" : C_FUNCTION, "return" : C_RETURN, "call" : C_CALL}

    def has_more_commands(self):
        while self.lines:
            self.next_line = self.lines.pop(POP_INDEX)
            self.next_line = " ".join(self.next_line.split())
            is_comment = self.next_line.startswith("//")

            # the current line is a comment or an empty line - continue to the next line
            # maybe to add a tab
            if (not is_comment) and (not self.next_line == " ") and (not self.next_line == ""):
                if "//" in self.next_line:
                    index = self.next_line.index("//")
                    self.next_line = self.next_line[:index]
                return True
        return False

    def advance(self):
        return self.next_line

    def command_type(self):
        if " " in self.next_line:
            sep = self.next_line.index(" ")
        else:
            sep = len(self.next_line)
        command = self.next_line[:sep]
        self.curr_type = self.commands_table[command]
        return self.curr_type

    def arg1(self):
        # C_ARITHMETIC
        if self.curr_type == C_ARITHMETIC:
            return self.next_line
        # C_PUSH or C_POP (if the command is one of those, it has at least two spaces)
        if (self.curr_type == C_POP) or (self.curr_type == C_PUSH):
            sep = self.next_line.index(" ")
            temp_line = self.next_line[sep + 1:]
            sep = temp_line.index(" ")
            return temp_line[:sep]
        return "null"

    def arg2(self):
         if (self.curr_type == C_POP) or (self.curr_type == C_PUSH):
             sep = self.next_line.index(" ")
             temp_line = self.next_line[sep + 1:]
             sep = temp_line.index(" ")
             return int (temp_line[sep + 1:])

