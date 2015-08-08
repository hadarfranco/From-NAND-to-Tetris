__author__ = 'francoland'


COMMENTS = ["//", "/*", "/**"]

COMMENT_OPEN_1 = "/*"
COMMENT_CLOSE_1 = "*/"
COMMENT_OPEN_2 = "/**"
COMMENT_OPEN_3 = "//"

CLASS = 0
METHOD = 1
FUNCTION = 2
CONSTRUCTOR = 3
INT = 4
BOOLEAN = 5
CHAR = 6
VOID = 7
VAR = 8
STATIC = 9
FIELD = 10
LET = 11
DO = 12
IF = 13
ELSE = 14
WHILE = 15
RETURN = 16
TRUE = 17
FALSE = 18
NULL = 19
THIS = 20

KEYWORD = 0
SYMBOL = 1
STRING_CONST = 2
INT_CONST = 3
IDENTIFIER = 4

POP_INDEX = 0

class JackTokenizer:

    def __init__(self, input_file):
        self.keyword_list = ["class", "method","function", "constructor", "int", "boolean", "char", "void", "var",
                            "static", "field", "let", "do", "if", "else", "while", "return", "true", "false", "null",
                             "this"]
        self.symbol_list = {"{" : "{" , "}" : "}", "(" : "(", ")" :  ")", "[" : "[", "]" : "]", ";" : ";", "." : "." ,
                            "," : "," ,
                            "+" : "+", "-" : "-", "*" : "*", "/" : "/", "&" : "&", "|" : "|", "<" : "<"
                            , ">" : ">", "=" : "=", "~" : "~"}
        self.input_file = open(input_file, "r")
        self.curr_line = ""
        self.curr_token = ""
        self.tokens_list = list()
        self.lines = self.input_file.readlines()
        self.parsed_lines = list()
        self.remove_comments()
        self.remove_white_spaces()
        self.add_white_spaces()

    def has_more_tokens(self):
        if self.tokens_list:
            return True
        elif self.lines:
            self.curr_line = self.lines.pop(POP_INDEX)
            self.split_into_tokens()
            return True
        self.input_file.close()
        return False

    def advance(self):
        self.curr_token = self.tokens_list.pop(POP_INDEX)

    def token_type(self):
        if self.curr_token in self.keyword_list:
            return KEYWORD
        if self.curr_token in self.symbol_list:
            return SYMBOL
        if self.curr_token.startswith("\""):
            return STRING_CONST
        if self.curr_token.isdigit():
            return INT_CONST
        return IDENTIFIER

    def key_word(self):
        return self.curr_token

    def symbol(self):
        return self.symbol_list[self.curr_token]

    def identifier(self):
        return self.curr_token

    def int_val(self):
        return self.curr_token

    def string_val(self):
        return self.curr_token[1:-1]



    def remove_comments(self):
        inside_comment = False
        self.parsed_lines = list()
        for line in self.lines:
            dic_index = {}
            count_quotes = 0
            i = 0
            length = len(line)
            start = 0
            enf = 0
            while True:
                if line[i] == "\"" and not inside_comment:
                    count_quotes += 1
                if line[i] == "/" and not inside_comment:
                    if count_quotes % 2 == 0:
                        if line[i + 1] == "/":
                            dic_index[i] = length
                            break
                        elif line[i + 1] == "*":
                            start = i
                            while i + 1 < length and not (line[i] == "*" and line[i + 1] == "/"):
                                i += 1
                            if i + 1 < length:
                                dic_index[start] = i + 2
                                i += 1
                            else:
                                dic_index[start] = length
                                inside_comment = True
                                break
                if inside_comment and line[i] == "*":
                    if i + 1 < length and line[i + 1] == "/":
                        dic_index[0] = i + 2
                        inside_comment = False
                # all the line is a comment
                elif inside_comment and i + 1 == length:
                    dic_index[0] = length
                i += 1
                if i >= length:
                    break
            parsed_line = ""
            start = 0
            while dic_index:
                end = min(dic_index)
                parsed_line += " " + line[start : end]
                start = dic_index[end]
                del dic_index[end]
            parsed_line += " " + line[start:length] + " "
            self.parsed_lines.append(parsed_line)
        self.lines = self.parsed_lines

    def add_white_spaces(self):
        self.parsed_lines = list()
        for line in self.lines:
            parsed_line = ""
            for i in range (len(line)):
                if line[i] in self.symbol_list and not self.is_inside_string(line,i):
                    parsed_line += " " + line[i] + " "
                else:
                    parsed_line += line[i]
            parsed_line = parsed_line.strip()
            self.parsed_lines.append(parsed_line)
        self.lines = self.parsed_lines

    def remove_white_spaces(self):
        self.parsed_lines = list()
        #remove white space
        for line in self.lines:
            # there is no string in the current line
            if "\"" not in line:
                parsed_line = " ".join(line.split())
            else:
                temp_line = line
                parsed_line = ""
                while "\"" in temp_line:
                    open_index = temp_line.find("\"")
                    close_index = temp_line[open_index + 1:].find("\"") + open_index + 1
                    without_spaces = " ".join(temp_line[:open_index].split())
                    parsed_line = parsed_line + without_spaces + temp_line[open_index:close_index+1]
                    temp_line = temp_line[close_index+1:]
                parsed_line = parsed_line + temp_line

            self.parsed_lines.append(parsed_line)
        # remove empty lines
        self.parsed_lines = [x for x in self.parsed_lines if (x != "\n" and x!="") ]
        self.lines = self.parsed_lines

    def is_inside_string(self, line, index):
        count_quotes = line[:index].count("\"")
        if count_quotes % 2 == 0:
            return False
        return True

    def split_into_tokens(self):
        temp_line = self.curr_line
        index = 0
        while index < len(temp_line):
            while temp_line[index] == " ":
                index += 1
            if temp_line[index] == "\"":
                token_ends = temp_line[index+1:].find("\"") + index + 1
                self.tokens_list.append(temp_line[index : token_ends+1])
                token_ends += 1
            else:
                token_ends = temp_line[index:].find(" ") + index
                if token_ends > -1 + index:
                    self.tokens_list.append(temp_line[index : token_ends])
                else:
                    self.tokens_list.append(temp_line[index :])
                    token_ends = len(temp_line)
            index = token_ends


















