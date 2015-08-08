__author__ = 'francoland'

from JackTokenizer import JackTokenizer
from JackTokenizer import KEYWORD, SYMBOL, IDENTIFIER, INT_CONST, STRING_CONST

from SymbolTable import SymbolTable
from SymbolTable import STATIC, FIELD, ARG, VAR, NONE

from VMWriter import VMWriter
from VMWriter import ARGUMENT, LCL, CONST, THIS, THAT, POINTER, TEMP

NUM_TOKENS_CLASS_DEC = 3
LIST = 5



class CompilationEngine:

    def __init__(self, input_file, output_file):
        self.jack_tokenizer = JackTokenizer(input_file)
        self.symbol_table = SymbolTable()
        self.writer = VMWriter(output_file)
        self.class_name = ""
        self.subroutine_name = ""
        self.return_type = ""
        self.label_counter_if = 0
        self.label_counter_while = 0
        self.num_args_called_function = 0
        self.is_unary = False
        self.dic_arithmetic = {"+" : "add" , "-" : "sub", "*" : "call Math.multiply 2",
                               "/" : "call Math.divide 2", "&" : "and", "|" : "or", "<" : "lt", ">" : "gt", "=" : "eq"}

    def compile_class(self):
        # "class className {
        for i in range(NUM_TOKENS_CLASS_DEC):
            self.jack_tokenizer.has_more_tokens()
            self.jack_tokenizer.advance()
            # saves the className
            if self.jack_tokenizer.token_type() == IDENTIFIER:
                self.class_name = self.jack_tokenizer.identifier()
        # classVarDec* or SubroutineDec*
        while self.jack_tokenizer.has_more_tokens():
            self.jack_tokenizer.advance()
            token_type = self.jack_tokenizer.token_type()
            if token_type == KEYWORD and (self.jack_tokenizer.key_word() == "static" or
                                                  self.jack_tokenizer.key_word() == "field"):
                self.compile_class_var_dec()
            if token_type == KEYWORD and (self.jack_tokenizer.key_word() == "function" or
                                                  self.jack_tokenizer.key_word() == "method" or
                                                  self.jack_tokenizer.key_word() == "constructor"):
                self.compile_subroutine()
            if token_type == SYMBOL and self.jack_tokenizer.symbol() == "}":
                break

    def compile_class_var_dec(self):
        # "static" of "field"
        kind = self.jack_tokenizer.key_word()
        self.jack_tokenizer.has_more_tokens()
        self.jack_tokenizer.advance()
        # type
        if self.jack_tokenizer.token_type() == KEYWORD:
            type = self.jack_tokenizer.key_word()
        else:
            type = self.jack_tokenizer.identifier()
        while self.jack_tokenizer.has_more_tokens():
            self.jack_tokenizer.advance()
            token_type = self.jack_tokenizer.token_type()
            if token_type == IDENTIFIER:
                name = self.jack_tokenizer.identifier()
                self.symbol_table.define(name,type,kind)
            elif token_type == SYMBOL:
                if self.jack_tokenizer.symbol() == ";":
                    break


    def compile_subroutine(self):
        self.symbol_table.start_subroutine()
        self.subroutine_name = ""
        self.return_type = ""
        self.label_counter_if = 0
        self.label_counter_while = 0
        #  the curr token : "constructor" or "function" or "method
        type_of_subroutine = self.jack_tokenizer.key_word()
        self.jack_tokenizer.has_more_tokens()
        self.jack_tokenizer.advance()
        # the curr token : return type of the subroutine
        if self.jack_tokenizer.token_type() == KEYWORD:
            self.return_type = self.jack_tokenizer.key_word()
        else:
            self.return_type = self.jack_tokenizer.identifier()
        self.jack_tokenizer.has_more_tokens()
        self.jack_tokenizer.advance()
        self.subroutine_name = self.jack_tokenizer.identifier()
        while self.jack_tokenizer.has_more_tokens():
            self.jack_tokenizer.advance()
            if self.jack_tokenizer.symbol() == "(":
                if type_of_subroutine == "method":
                    self.symbol_table.define(THIS, self.class_name, ARG)
                self.compile_parameter_list()
                # the curr token should be -  ")"
            if self.jack_tokenizer.symbol() == '{':
                while self.jack_tokenizer.has_more_tokens():
                    self.jack_tokenizer.advance()
                    token_type = self.jack_tokenizer.token_type()
                    if token_type == KEYWORD:
                        if self.jack_tokenizer.key_word() == "var":
                            self.compile_var_dec()
                            continue
                        else:
                            self.writer.write_function(self.class_name +
                                                       "." + self.subroutine_name, self.symbol_table.var_count(VAR))
                            if type_of_subroutine == "constructor":
                                self.writer.write_push(CONST, self.symbol_table.var_count(FIELD))
                                self.writer.write_call("Memory.alloc", 1)
                                self.writer.write_pop("pointer", 0)
                            elif type_of_subroutine == "method":
                                self.writer.write_push(ARGUMENT, 0)
                                self.writer.write_pop("pointer", 0)
                            self.compile_statements()
                            # the curr token should be -  "}"
                            break
                break


    def compile_parameter_list(self):
        kind = ARG
        while self.jack_tokenizer.has_more_tokens():
            self.jack_tokenizer.advance()
            token_type = self.jack_tokenizer.token_type()
            # int, bool....
            if token_type == KEYWORD:
                type = self.jack_tokenizer.key_word()
                self.jack_tokenizer.has_more_tokens()
                self.jack_tokenizer.advance()
                name = self.jack_tokenizer.identifier()
                self.symbol_table.define(name, type, kind)
            # className
            elif token_type == IDENTIFIER:
                type = self.jack_tokenizer.identifier()
                self.jack_tokenizer.has_more_tokens()
                self.jack_tokenizer.advance()
                name = self.jack_tokenizer.identifier()
                self.symbol_table.define(name, type, kind)
            # end of parameter list
            if token_type == SYMBOL and self.jack_tokenizer.symbol() == ")":
                    break


    def compile_var_dec(self):
        # should be "var"
        kind = self.jack_tokenizer.key_word()
        self.jack_tokenizer.has_more_tokens()
        self.jack_tokenizer.advance()
        # type
        if self.jack_tokenizer.token_type() == KEYWORD:
            type = self.jack_tokenizer.key_word()
        else:
            type = self.jack_tokenizer.identifier()
        while self.jack_tokenizer.has_more_tokens():
            self.jack_tokenizer.advance()
            token_type = self.jack_tokenizer.token_type()
            if token_type == IDENTIFIER:
                name = self.jack_tokenizer.identifier()
                self.symbol_table.define(name, type, kind)
            if token_type == SYMBOL:
                if self.jack_tokenizer.symbol() == ";":
                    break


    def compile_statements(self):
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
            # compile_if returns advanced
            if self.jack_tokenizer.token_type() == KEYWORD and self.jack_tokenizer.key_word() == "if":
                self.compile_if()
            if self.jack_tokenizer.token_type() == SYMBOL and self.jack_tokenizer.symbol() == "}":
                break


    def compile_do(self):
        self.num_args_called_function = 0
        self.compile_subroutine_call()
        self.writer.write_pop(TEMP , 0)
        self.jack_tokenizer.has_more_tokens()
        self.jack_tokenizer.advance()
        # return from compile_subroutine_call with ";"

    def compile_let(self):
        init = True
         # the curr token - "let"
        while self.jack_tokenizer.has_more_tokens():
            self.jack_tokenizer.advance()
            token_type = self.jack_tokenizer.token_type()
            if token_type == IDENTIFIER:
                name = self.jack_tokenizer.identifier()
                type = self.symbol_table.type_of(name)
                kind = self.symbol_table.kind_of(name)
                index = self.symbol_table.index_of(name)
            if token_type == SYMBOL:
                # there is an assignment to an array
                if self.jack_tokenizer.symbol() == "[":
                    self.jack_tokenizer.has_more_tokens()
                    self.jack_tokenizer.advance()
                    #  handle  - [expression]
                    self.compile_expression()
                    # the curr token -  "]"
                    self.writer.write_push(self.find_segment(kind), index)
                    self.writer.write_arithmetic("add")
                    self.writer.write_pop("pointer", 1)
                    init = False
                # should return from the compile_expression only with ";" or "]"
                if self.jack_tokenizer.symbol() == "=":
                    self.jack_tokenizer.has_more_tokens()
                    self.jack_tokenizer.advance()
                    # handle the = expression
                    self.compile_expression()
                    # that is only for array
                    if init == False: # was also if type == "Array"
                        self.writer.write_pop(THAT, 0)
                    else:
                        self.writer.write_pop(self.find_segment(kind), index)
                # end of let statement
                if self.jack_tokenizer.symbol() == ";":
                    break


    def compile_while(self):
        while_counter = self.label_counter_while
        self.label_counter_while += 1
        # the curr token - "while"
        self.writer.write_label("WHILE_EXP" + str(while_counter))
        while self.jack_tokenizer.has_more_tokens():
            self.jack_tokenizer.advance()
            token_type = self.jack_tokenizer.token_type()
            if token_type == SYMBOL:
                if self.jack_tokenizer.symbol() == "(":
                    self.jack_tokenizer.has_more_tokens()
                    self.jack_tokenizer.advance()
                    self.compile_expression()
                    # the curr token - ")"
                    self.writer.write_arithmetic("not")
                    self.writer.write_if("WHILE_END" + str(while_counter))
                if self.jack_tokenizer.symbol() == "{":
                    self.jack_tokenizer.has_more_tokens()
                    self.jack_tokenizer.advance()
                    self.compile_statements()
                    # the curr token - "}"
                    self.writer.write_go_to("WHILE_EXP" + str(while_counter))
                    self.writer.write_label("WHILE_END" + str(while_counter))
                if token_type == SYMBOL and self.jack_tokenizer.symbol() == "}":
                    break


    def compile_return(self):
        # the curr token - "return"
        self.jack_tokenizer.has_more_tokens()
        self.jack_tokenizer.advance()
        if self.jack_tokenizer.token_type() == SYMBOL and self.jack_tokenizer.symbol() == ";":
            self.writer.write_push(CONST, "0")
        else:
            self.compile_expression()
            # should return from "compile_expression" only with ";"
        self.writer.write_return()

    def compile_if(self):
        if_counter = self.label_counter_if
        self.label_counter_if += 1
        # the curr token - "if"
        while self.jack_tokenizer.has_more_tokens():
            self.jack_tokenizer.advance()
            token_type = self.jack_tokenizer.token_type()
            if token_type == SYMBOL:
                if self.jack_tokenizer.symbol() == "(":
                    self.jack_tokenizer.has_more_tokens()
                    self.jack_tokenizer.advance()
                    self.compile_expression()
                    # the curr token - ")"
                    self.writer.write_if("IF_TRUE" + str(if_counter))
                    self.writer.write_go_to("IF_FALSE" + str(if_counter))
                if self.jack_tokenizer.token_type() == SYMBOL and self.jack_tokenizer.symbol() == "{":
                    self.writer.write_label("IF_TRUE" + str(if_counter))
                    self.jack_tokenizer.has_more_tokens()
                    self.jack_tokenizer.advance()
                    self.compile_statements()
                # ~~~~~~~~~~ change : was token_type ~~~~~~~~~~~~~~
                if self.jack_tokenizer.token_type() == SYMBOL and self.jack_tokenizer.symbol() == "}":
                    break
        self.jack_tokenizer.has_more_tokens()
        self.jack_tokenizer.advance()
        if self.jack_tokenizer.token_type() == KEYWORD and self.jack_tokenizer.key_word() == "else":
            # print "else"
            self.writer.write_go_to("IF_END" + str(if_counter))
            self.writer.write_label("IF_FALSE" + str(if_counter))
            self.jack_tokenizer.has_more_tokens()
            self.jack_tokenizer.advance()
            # print "{"
            self.jack_tokenizer.has_more_tokens()
            self.jack_tokenizer.advance()
            self.compile_statements()
            # print "}"
            self.jack_tokenizer.has_more_tokens()
            self.jack_tokenizer.advance()
            self.writer.write_label("IF_END" + str(if_counter))
        else:
            self.writer.write_label("IF_FALSE" + str(if_counter))


    def compile_subroutine_call(self):
        to_add = False
        self.jack_tokenizer.has_more_tokens()
        self.jack_tokenizer.advance()
        # "subRoutineName" or ("className" | "varName", as part of className.subRoutineName)
        called_statement = self.jack_tokenizer.identifier()
        type = self.symbol_table.type_of(called_statement)
        kind = self.symbol_table.kind_of(called_statement)
        index = self.symbol_table.index_of(called_statement)


        self.jack_tokenizer.has_more_tokens()
        self.jack_tokenizer.advance()
        # case of "subRoutineCall(expressionList)
        if self.jack_tokenizer.token_type() == SYMBOL and self.jack_tokenizer.symbol() == "(":
            to_add = True
            called_statement = self.class_name + "." + called_statement
            self.writer.write_push(POINTER, 0)
            self.compile_expression_list()
            # the curr token - ")"
        # (className | varName).subroutineName(expressionList)
        elif self.jack_tokenizer.token_type() == SYMBOL and self.jack_tokenizer.symbol() == ".":
            self.jack_tokenizer.has_more_tokens()
            self.jack_tokenizer.advance()
            # subroutineName
            if kind <> NONE:
                to_add = True
                self.writer.write_push(self.find_segment(kind), index)
                called_statement = type + "." + self.jack_tokenizer.identifier()
            else:
               called_statement = called_statement + "." + self.jack_tokenizer.identifier()
            self.jack_tokenizer.has_more_tokens()
            self.jack_tokenizer.advance()
            # "("
            # expressionList
            self.compile_expression_list()
            # ")"
        if to_add:
            self.writer.write_call(called_statement, self.num_args_called_function + 1)
        else:
            self.writer.write_call(called_statement, self.num_args_called_function)

    def compile_expression(self):
        is_print_unary = False
        if self.jack_tokenizer.token_type() == SYMBOL and self.jack_tokenizer.symbol() == "-":
            self.is_unary = True
        self.compile_term()
        while self.jack_tokenizer.token_type() == SYMBOL and self.jack_tokenizer.symbol() in\
                ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
            arit_symbol = self.jack_tokenizer.symbol()
            self.jack_tokenizer.has_more_tokens()
            self.jack_tokenizer.advance()
            if self.jack_tokenizer.token_type() == SYMBOL and self.jack_tokenizer.symbol() == "-":
                self.is_unary = True
                is_print_unary = True
            self.compile_term()
            # if not is_print_unary and
            self.writer.write_arithmetic(self.dic_arithmetic[arit_symbol])


    def compile_term(self):
        while True:
            token_type = self.jack_tokenizer.token_type()
            if token_type == SYMBOL and not self.is_unary and self.jack_tokenizer.symbol() in\
                    [",", ";", ")", "}","]", "+", "-", "*", "/", "&", "|", "<", ">", "="]:
                break
            if token_type == INT_CONST:
                self.writer.write_push(CONST, self.jack_tokenizer.int_val())
                self.jack_tokenizer.has_more_tokens()
                self.jack_tokenizer.advance()
                break
            if token_type == STRING_CONST:
                self.compile_string()
                self.jack_tokenizer.has_more_tokens()
                self.jack_tokenizer.advance()
                break
            if token_type == KEYWORD and self.jack_tokenizer.key_word() in ["true", "false", "null"]:
                self.writer.write_push(CONST, 0)
                if self.jack_tokenizer.key_word() == "true":
                    self.writer.write_arithmetic("not")
                self.jack_tokenizer.has_more_tokens()
                self.jack_tokenizer.advance()
                break
            # like in return this
            if token_type == KEYWORD and self.jack_tokenizer.key_word() == "this":
                self.writer.write_push(POINTER, 0)
                self.jack_tokenizer.has_more_tokens()
                self.jack_tokenizer.advance()
                break
            if token_type == SYMBOL and self.jack_tokenizer.symbol() in ["~", "-"]:
                symbol = self.jack_tokenizer.symbol()
                self.is_unary = False
                self.jack_tokenizer.has_more_tokens()
                self.jack_tokenizer.advance()
                self.compile_term()
                if symbol == "~":
                    self.writer.write_arithmetic("not")
                else:
                    self.writer.write_arithmetic("neg")
                break
            if token_type == SYMBOL and self.jack_tokenizer.symbol() == "(":
                self.jack_tokenizer.has_more_tokens()
                self.jack_tokenizer.advance()
                self.compile_expression()
                # should return from compile_expression only with ")"
                self.jack_tokenizer.has_more_tokens()
                self.jack_tokenizer.advance()
                break
            if token_type == IDENTIFIER:
                is_add = True
                name = self.jack_tokenizer.identifier()
                kind = self.symbol_table.kind_of(name)
                index = self.symbol_table.index_of(name)
                if name[0].isupper():
                    is_add = False
                self.jack_tokenizer.has_more_tokens()
                self.jack_tokenizer.advance()
                if self.jack_tokenizer.token_type() == SYMBOL and self.jack_tokenizer.symbol() in\
                        [",", ";", ")", "}","]", "+", "-", "*", "/", "&", "|", "<", ">", "=", "&amp;", "&lt;","&gt;"]:
                    # in case of a > ...or b;
                    self.writer.write_push(self.find_segment(kind), self.symbol_table.index_of(name))
                    break
                if self.jack_tokenizer.token_type() == SYMBOL and self.jack_tokenizer.symbol() == "[":
                    self.jack_tokenizer.has_more_tokens()
                    self.jack_tokenizer.advance()
                    self.compile_expression()
                    # should return only "]"
                    self.writer.write_push(self.find_segment(kind), self.symbol_table.index_of(name))
                    self.writer.write_arithmetic("add")
                    self.writer.write_pop(POINTER, 1)
                    self.writer.write_push(THAT, 0)
                    self.jack_tokenizer.has_more_tokens()
                    self.jack_tokenizer.advance()
                    break
                if self.jack_tokenizer.token_type() == SYMBOL and self.jack_tokenizer.symbol() == "(":
                    self.writer.write_push(POINTER, 0)
                    self.compile_expression_list()
                    self.jack_tokenizer.has_more_tokens()
                    self.jack_tokenizer.advance()
                    # case of a = ... bar()
                    self.writer.write_call(self.class_name + "." + name,self.num_args_called_function + 1)
                    break
                # (className | varName).subroutineName(expressionList)
                if self.jack_tokenizer.token_type() == SYMBOL and self.jack_tokenizer.symbol() == ".":
                    self.jack_tokenizer.has_more_tokens()
                    self.jack_tokenizer.advance()
                    # subroutineName
                    if is_add:
                        type = self.symbol_table.type_of(name)
                        name = type + "." + self.jack_tokenizer.identifier()
                    else:
                        name = name + "." + self.jack_tokenizer.identifier()
                    self.jack_tokenizer.has_more_tokens()
                    self.jack_tokenizer.advance()
                    # "("
                    # expressionList
                    if is_add:
                        self.writer.write_push(self.find_segment(kind), index)
                    self.compile_expression_list()
                    # ")"
                    if is_add:
                        self.writer.write_call(name, self.num_args_called_function + 1)
                    else:
                        self.writer.write_call(name, self.num_args_called_function)
            self.jack_tokenizer.has_more_tokens()
            self.jack_tokenizer.advance()

    def compile_expression_list(self):
        num_args = 0
        while self.jack_tokenizer.has_more_tokens():
            self.jack_tokenizer.advance()
            if self.jack_tokenizer.token_type() == SYMBOL and self.jack_tokenizer.symbol() == ")":
                break
            else:
                num_args += 1
                self.compile_expression()
                if self.jack_tokenizer.symbol() == ")":
                    break
                # print ","
        self.num_args_called_function = num_args

    def find_segment(self, kind):
        if kind == ARG:
            return ARGUMENT
        if kind == VAR:
            return LCL
        if kind == FIELD:
            return THIS
        if kind == STATIC:
            return STATIC

    def compile_string(self):
        length = len(self.jack_tokenizer.string_val())
        self.writer.write_push(CONST, length)
        self.writer.write_call("String.new", 1)
        for i in range(len(self.jack_tokenizer.string_val())):
            uni = ord(self.jack_tokenizer.string_val()[i])
            self.writer.write_push(CONST, uni)
            self.writer.write_call("String.appendChar", 2)







