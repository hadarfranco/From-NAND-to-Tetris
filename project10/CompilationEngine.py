__author__ = 'francoland'

from JackTokenizer import JackTokenizer
from JackTokenizer import KEYWORD, SYMBOL, IDENTIFIER, INT_CONST, STRING_CONST

NUM_TOKENS_CLASS_DEC = 3
LIST = 5


class CompilationEngine:

    def __init__(self, input_file, output_file):
        self.jack_tokenizer = JackTokenizer(input_file)
        self.output = open(output_file, "w")
        self.level = 0
        self.is_unary = False

    def compile_class(self):
        self.print_title("class", True)
        self.level += 1
        # "class className {
        for i in range(NUM_TOKENS_CLASS_DEC):
            self.jack_tokenizer.has_more_tokens()
            self.jack_tokenizer.advance()
            token_type = self.jack_tokenizer.token_type()
            if token_type == KEYWORD:
                self.print_tag(token_type, self.jack_tokenizer.key_word())
            if token_type == IDENTIFIER:
                self.print_tag(token_type, self.jack_tokenizer.identifier())
            if token_type == SYMBOL:
                self.print_tag(token_type, self.jack_tokenizer.symbol())
        # classVarDec* or SubroutineDec*
        while self.jack_tokenizer.has_more_tokens():
            self.jack_tokenizer.advance()
            token_type = self.jack_tokenizer.token_type()
            curr_keyword = self.jack_tokenizer.key_word()
            if token_type == KEYWORD and (self.jack_tokenizer.key_word() == "static" or
                                                  self.jack_tokenizer.key_word() == "field"):
                self.compile_class_var_dec()
            if token_type == KEYWORD and (self.jack_tokenizer.key_word() == "function" or
                                                  self.jack_tokenizer.key_word() == "method" or
                                                  self.jack_tokenizer.key_word() == "constructor"):
                self.compile_subroutine()
                # self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
                # break
            if token_type == SYMBOL and self.jack_tokenizer.symbol() == "}":
                self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
                break
        self.level -= 1
        self.print_title("class", False)

    def compile_class_var_dec(self):
        self.print_title("classVarDec", True)
        self.level += 1
        # "static" or "field"
        self.print_tag(KEYWORD, self.jack_tokenizer.key_word())
        while self.jack_tokenizer.has_more_tokens():
            self.jack_tokenizer.advance()
            token_type = self.jack_tokenizer.token_type()
            if token_type == KEYWORD:
                self.print_tag(token_type, self.jack_tokenizer.key_word())
            elif token_type == IDENTIFIER:
                self.print_tag(token_type, self.jack_tokenizer.identifier())
            elif token_type == SYMBOL:
                self.print_tag(token_type, self.jack_tokenizer.symbol())
                if self.jack_tokenizer.symbol() == ";":
                    break
        self.level -= 1
        self.print_title("classVarDec", False)


    def compile_subroutine(self):
        self.print_title("subroutineDec", True)
        self.level += 1
        # "constructor" or "function" or "method"
        self.print_tag(KEYWORD, self.jack_tokenizer.key_word())
        while self.jack_tokenizer.has_more_tokens():
            self.jack_tokenizer.advance()
            token_type = self.jack_tokenizer.token_type()
            if token_type == KEYWORD:
                self.print_tag(KEYWORD, self.jack_tokenizer.key_word())
            elif token_type == IDENTIFIER:
                self.print_tag(IDENTIFIER, self.jack_tokenizer.identifier())
            elif token_type == SYMBOL:
                if self.jack_tokenizer.symbol() == "(":
                    self.print_tag(token_type, self.jack_tokenizer.symbol())
                    self.compile_parameter_list()
                    # should print ")"
                    self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
                # if self.jack_tokenizer.symbol() == "}":
                #     break
                if self.jack_tokenizer.symbol() == '{':
                    self.compile_subroutine_body()
                    break
        self.level -= 1
        self.print_title("subroutineDec", False)

    def compile_subroutine_body(self):
        self.print_title("subroutineBody", True)
        self.level += 1
        self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
        while self.jack_tokenizer.has_more_tokens():
            self.jack_tokenizer.advance()
            token_type = self.jack_tokenizer.token_type()
            if token_type == SYMBOL:
                self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
            if token_type == KEYWORD:
                if self.jack_tokenizer.key_word() == "var":
                    self.compile_var_dec()
                    continue
                else:
                    self.compile_statements()
                    # print "}"
                    self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
                    break
        self.level -= 1
        self.print_title("subroutineBody", False)


    def compile_parameter_list(self):
        self.print_title("parameterList", True)
        self.level += 1
        while self.jack_tokenizer.has_more_tokens():
            self.jack_tokenizer.advance()
            token_type = self.jack_tokenizer.token_type()
            if token_type == KEYWORD:
                self.print_tag(KEYWORD, self.jack_tokenizer.key_word())
            elif token_type == IDENTIFIER:
                self.print_tag(IDENTIFIER, self.jack_tokenizer.identifier())
            else:
                if self.jack_tokenizer.symbol() == ")":
                    break
                else:
                    self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
        self.level -= 1
        self.print_title("parameterList", False)


    def compile_var_dec(self):
        self.print_title("varDec", True)
        self.level += 1
        self.print_tag(KEYWORD, self.jack_tokenizer.key_word())
        while self.jack_tokenizer.has_more_tokens():
            self.jack_tokenizer.advance()
            token_type = self.jack_tokenizer.token_type()
            if token_type == KEYWORD:
                self.print_tag(KEYWORD, self.jack_tokenizer.key_word())
            if token_type == IDENTIFIER:
                self.print_tag(IDENTIFIER, self.jack_tokenizer.identifier())
            if token_type == SYMBOL:
                self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
                if self.jack_tokenizer.symbol() == ";":
                    break
        self.level -= 1
        self.print_title("varDec", False)


    def compile_statements(self):
        self.print_title("statements", True)
        self.level += 1
        while True:
            if self.jack_tokenizer.token_type() == KEYWORD and self.jack_tokenizer.key_word() == "do":
                self.compile_do()
                self.jack_tokenizer.has_more_tokens()
                self.jack_tokenizer.advance()
            if self.jack_tokenizer.token_type() == KEYWORD and self.jack_tokenizer.key_word() == "let":
                self.compile_let()
                self.jack_tokenizer.has_more_tokens()
                self.jack_tokenizer.advance()
            if self.jack_tokenizer.token_type() == KEYWORD and self.jack_tokenizer.key_word() == "while":
                self.compile_while()
                self.jack_tokenizer.has_more_tokens()
                self.jack_tokenizer.advance()
            if self.jack_tokenizer.token_type() == KEYWORD and self.jack_tokenizer.key_word() == "return":
                self.compile_return()
                self.jack_tokenizer.has_more_tokens()
                self.jack_tokenizer.advance()
            if self.jack_tokenizer.token_type() == KEYWORD and self.jack_tokenizer.key_word() == "if":
                self.compile_if()
            if self.jack_tokenizer.token_type() == SYMBOL and self.jack_tokenizer.symbol() == "}":
                break
        self.level -= 1
        self.print_title("statements", False)


    def compile_do(self):
        self.print_title("doStatement", True)
        self.level += 1
        self.print_tag(KEYWORD, self.jack_tokenizer.key_word())
        self.compile_subroutine_call()
        self.jack_tokenizer.has_more_tokens()
        self.jack_tokenizer.advance()
        # return from compile_subroutine_call with ";"
        self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
        self.level -= 1
        self.print_title("doStatement", False)

    def compile_let(self):
        self.print_title("letStatement", True)
        self.level += 1
        self.print_tag(KEYWORD, self.jack_tokenizer.key_word())
        while self.jack_tokenizer.has_more_tokens():
            self.jack_tokenizer.advance()
            token_type = self.jack_tokenizer.token_type()
            if token_type == IDENTIFIER:
                self.print_tag(IDENTIFIER, self.jack_tokenizer.identifier())
                #continue
            if token_type == SYMBOL:
                if self.jack_tokenizer.symbol() == "[":# or self.jack_tokenizer.symbol() == "=":
                    self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
                    self.jack_tokenizer.has_more_tokens()
                    self.jack_tokenizer.advance()
                    self.compile_expression()
                    # print "]"
                    self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
                # should return from the compile_expression only with ";" or "]"
                if self.jack_tokenizer.symbol() == "=":
                    self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
                    self.jack_tokenizer.has_more_tokens()
                    self.jack_tokenizer.advance()
                    self.compile_expression()
                if self.jack_tokenizer.symbol() == ";":
                    self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
                    break
        self.level -= 1
        self.print_title("letStatement", False)

    def compile_while(self):
        self.print_title("whileStatement", True)
        self.level += 1
        self.print_tag(KEYWORD, self.jack_tokenizer.key_word())
        while self.jack_tokenizer.has_more_tokens():
            self.jack_tokenizer.advance()
            token_type = self.jack_tokenizer.token_type()
            if token_type == SYMBOL:
                if self.jack_tokenizer.symbol() == "(":
                    self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
                    self.jack_tokenizer.has_more_tokens()
                    self.jack_tokenizer.advance()
                    self.compile_expression()
                if self.jack_tokenizer.symbol() == "{":
                    self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
                    self.jack_tokenizer.has_more_tokens()
                    self.jack_tokenizer.advance()
                    self.compile_statements()
                self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
                if token_type == SYMBOL and self.jack_tokenizer.symbol() == "}":
                    break
        self.level -= 1
        self.print_title("whileStatement", False)


    def compile_return(self):
        self.print_title("returnStatement", True)
        self.level += 1
        self.print_tag(KEYWORD, self.jack_tokenizer.key_word())
        self.jack_tokenizer.has_more_tokens()
        self.jack_tokenizer.advance()
        if self.jack_tokenizer.token_type() == SYMBOL and self.jack_tokenizer.symbol() == ";":
            self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
        else:
            self.compile_expression()
            # should return from "compile_expression" only with ";"
            self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
        self.level -= 1
        self.print_title("returnStatement", False)

    def compile_if(self):
        self.print_title("ifStatement", True)
        self.level += 1
        self.print_tag(KEYWORD, self.jack_tokenizer.key_word())
        while self.jack_tokenizer.has_more_tokens():
            self.jack_tokenizer.advance()
            token_type = self.jack_tokenizer.token_type()
            if token_type == SYMBOL:
                if self.jack_tokenizer.symbol() == "(":
                    self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
                    self.jack_tokenizer.has_more_tokens()
                    self.jack_tokenizer.advance()
                    self.compile_expression()
                if self.jack_tokenizer.symbol() == "{":
                    self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
                    self.jack_tokenizer.has_more_tokens()
                    self.jack_tokenizer.advance()
                    self.compile_statements()
                self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
                if token_type == SYMBOL and self.jack_tokenizer.symbol() == "}":
                    break
        self.jack_tokenizer.has_more_tokens()
        self.jack_tokenizer.advance()
        if self.jack_tokenizer.token_type() == KEYWORD and self.jack_tokenizer.key_word() == "else":
            # print "else"
            self.print_tag(KEYWORD, self.jack_tokenizer.key_word())
            self.jack_tokenizer.has_more_tokens()
            self.jack_tokenizer.advance()
            # print "{"
            self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
            self.jack_tokenizer.has_more_tokens()
            self.jack_tokenizer.advance()
            self.compile_statements()
            # print "}"
            self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
            self.jack_tokenizer.has_more_tokens()
            self.jack_tokenizer.advance()
        self.level -= 1
        self.print_title("ifStatement", False)

    def compile_subroutine_call(self):
        self.jack_tokenizer.has_more_tokens()
        self.jack_tokenizer.advance()
        self.print_tag(IDENTIFIER, self.jack_tokenizer.identifier())
        self.jack_tokenizer.has_more_tokens()
        self.jack_tokenizer.advance()
        if self.jack_tokenizer.token_type() == SYMBOL and self.jack_tokenizer.symbol() == "(":
            self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
            self.compile_expression_list()
            self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
        # (className | varName).subroutineName(expressionList)
        elif self.jack_tokenizer.token_type() == SYMBOL and self.jack_tokenizer.symbol() == ".":
            self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
            self.jack_tokenizer.has_more_tokens()
            self.jack_tokenizer.advance()
            # subroutineName
            self.print_tag(IDENTIFIER, self.jack_tokenizer.identifier())
            self.jack_tokenizer.has_more_tokens()
            self.jack_tokenizer.advance()
            # "("
            self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
            # expressionList
            self.compile_expression_list()
            # ")"
            self.print_tag(SYMBOL, self.jack_tokenizer.symbol())


    def compile_expression(self):
        self.print_title("expression", True)
        self.level += 1
        if self.jack_tokenizer.token_type() == SYMBOL and self.jack_tokenizer.symbol() == "-":
            self.is_unary = True
        self.compile_term()
        while self.jack_tokenizer.token_type() == SYMBOL and self.jack_tokenizer.symbol() in\
                ["+", "-", "*", "/", "&", "|", "<", ">", "=", "&amp;", "&lt;","&gt;"]:
            self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
            self.jack_tokenizer.has_more_tokens()
            self.jack_tokenizer.advance()
            if self.jack_tokenizer.token_type() == SYMBOL and self.jack_tokenizer.symbol() == "-":
                self.is_unary = True
            self.compile_term()
        self.level -= 1
        self.print_title("expression", False)

    def compile_term(self):
        keywords_list = ["true", "false", "null", "this"]
        self.print_title("term", True)
        self.level += 1
        while True:
            token_type = self.jack_tokenizer.token_type()
            if token_type == SYMBOL and not self.is_unary and self.jack_tokenizer.symbol() in\
                    [",", ";", ")", "}","]", "+", "-", "*", "/", "&", "|", "<", ">", "=", "&amp;", "&lt;","&gt;"]:
                break
            if token_type == INT_CONST:
                self.print_tag(INT_CONST, self.jack_tokenizer.int_val())
                self.jack_tokenizer.has_more_tokens()
                self.jack_tokenizer.advance()
                break
            if token_type == STRING_CONST:
                self.print_tag(STRING_CONST, self.jack_tokenizer.string_val())
                self.jack_tokenizer.has_more_tokens()
                self.jack_tokenizer.advance()
                break
            if token_type == KEYWORD and self.jack_tokenizer.key_word() in keywords_list:
                self.print_tag(KEYWORD, self.jack_tokenizer.key_word())
                self.jack_tokenizer.has_more_tokens()
                self.jack_tokenizer.advance()
                break
            if token_type == SYMBOL and self.jack_tokenizer.symbol() in ["~", "-"]:
                self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
                self.is_unary = False
                self.jack_tokenizer.has_more_tokens()
                self.jack_tokenizer.advance()
                self.compile_term()
                break
            if token_type == SYMBOL and self.jack_tokenizer.symbol() == "(":
                self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
                self.jack_tokenizer.has_more_tokens()
                self.jack_tokenizer.advance()
                self.compile_expression()
                # should return from compile_expression only with ")"
                self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
                self.jack_tokenizer.has_more_tokens()
                self.jack_tokenizer.advance()
                break
            if token_type == IDENTIFIER:
                self.print_tag(IDENTIFIER, self.jack_tokenizer.identifier())
                self.jack_tokenizer.has_more_tokens()
                self.jack_tokenizer.advance()
                if self.jack_tokenizer.token_type() == SYMBOL and self.jack_tokenizer.symbol() in\
                        [",", ";", ")", "}","]", "+", "-", "*", "/", "&", "|", "<", ">", "=", "&amp;", "&lt;","&gt;"]:
                    break
                if self.jack_tokenizer.token_type() == SYMBOL and self.jack_tokenizer.symbol() == "[":
                    self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
                    self.jack_tokenizer.has_more_tokens()
                    self.jack_tokenizer.advance()
                    self.compile_expression()
                    # should print only "]"
                    self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
                    self.jack_tokenizer.has_more_tokens()
                    self.jack_tokenizer.advance()
                    break
                if self.jack_tokenizer.token_type() == SYMBOL and self.jack_tokenizer.symbol() == "(":
                    self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
                    self.compile_expression_list()
                    self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
                    self.jack_tokenizer.has_more_tokens()
                    self.jack_tokenizer.advance()
                    break
                # (className | varName).subroutineName(expressionList)
                if self.jack_tokenizer.token_type() == SYMBOL and self.jack_tokenizer.symbol() == ".":
                    self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
                    self.jack_tokenizer.has_more_tokens()
                    self.jack_tokenizer.advance()
                    # subroutineName
                    self.print_tag(IDENTIFIER, self.jack_tokenizer.identifier())
                    self.jack_tokenizer.has_more_tokens()
                    self.jack_tokenizer.advance()
                    # "("
                    self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
                    # expressionList
                    self.compile_expression_list()
                    # ")"
                    self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
            self.jack_tokenizer.has_more_tokens()
            self.jack_tokenizer.advance()
        self.level -= 1
        self.print_title("term", False)

    def compile_expression_list(self):
        self.print_title("expressionList", True)
        self.level += 1
        while self.jack_tokenizer.has_more_tokens():
            self.jack_tokenizer.advance()
            if self.jack_tokenizer.token_type() == SYMBOL and self.jack_tokenizer.symbol() == ")":
                break
            else:
                self.compile_expression()
                if self.jack_tokenizer.symbol() == ")":
                    break
                # print ","
                self.print_tag(SYMBOL, self.jack_tokenizer.symbol())
        self.level -= 1
        self.print_title("expressionList", False)


    def print_tag(self, token_type, value):
        tabs = ""
        tag = ""
        for i in range(self.level):
            tabs += "\t"
        if token_type == KEYWORD:
           tag = "<keyword> " + value + " </keyword>\n"
        elif token_type == SYMBOL:
            tag = "<symbol> " + value + " </symbol>\n"
        elif token_type == IDENTIFIER:
            tag = "<identifier> " + value + " </identifier>\n"
        elif token_type == INT_CONST:
            tag = "<integerConstant> " + value + " </integerConstant>\n"
        elif token_type == STRING_CONST:
            tag = "<stringConstant> " + value + " </stringConstant>\n"
        else:
            tag = "<" + value + ">" + " </" + value + ">\n"
        self.output.write(tabs + tag)

    def print_title(self, title, is_title):
        tabs = ""
        for i in range(self.level):
            tabs += "\t"
        if is_title:
            self.output.write(tabs + "<" + title + ">\n")
        # print closer
        else:
            self.output.write(tabs + "</" + title + ">\n")

