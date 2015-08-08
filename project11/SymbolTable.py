__author__ = 'francoland'

TYPE_POS = 0
KIND_POS = 1
INDEX_POS = 2

STATIC_POS = 0
FIELD_POS = 1
ARG_POS = 2
VAR_POS = 3

STATIC = "static"
FIELD = "field"
ARG = "arg"
VAR = "var"
NONE = "none"

class SymbolTable:

    def __init__(self):
        self.class_scope_table = {}
        self.subroutine_scope_table = {}
        self.indexes = [0, 0, 0, 0]


    def start_subroutine(self):
        self.subroutine_scope_table.clear()
        self.indexes[ARG_POS] = 0
        self.indexes[VAR_POS] = 0


    def define(self, name, type, kind):
        # the identifier is in the class scope
        if kind == STATIC:
            self.class_scope_table[name] = [type, kind, self.indexes[STATIC_POS]]
            self.indexes[STATIC_POS] += 1
        elif kind == FIELD:
            self.class_scope_table[name] = [type, kind, self.indexes[FIELD_POS]]
            self.indexes[FIELD_POS] += 1
        elif kind == VAR:
            self.subroutine_scope_table[name] = [type, kind, self.indexes[VAR_POS]]
            self.indexes[VAR_POS] += 1
        else:
            self.subroutine_scope_table[name] = [type, kind, self.indexes[ARG_POS]]
            self.indexes[ARG_POS] += 1

    def var_count(self, kind):
        if kind == STATIC or kind == FIELD:
            values = self.class_scope_table.values()
        else:
            values = self.subroutine_scope_table.values()
        counter = 0
        for v in values:
            if v[KIND_POS] == kind:
                counter += 1
        return counter

    def kind_of(self, name):
        if self.subroutine_scope_table.has_key(name):
            value = self.subroutine_scope_table[name]
            return value[KIND_POS]
        elif self.class_scope_table.has_key(name):
            value = self.class_scope_table[name]
            return value[KIND_POS]
        return NONE

    def type_of(self, name):
        if self.subroutine_scope_table.has_key(name):
            value = self.subroutine_scope_table[name]
            return value[TYPE_POS]
        elif self.class_scope_table.has_key(name):
            value = self.class_scope_table[name]
            return value[TYPE_POS]
        return NONE

    def index_of(self, name):
        if self.subroutine_scope_table.has_key(name):
            value = self.subroutine_scope_table[name]
            return value[INDEX_POS]
        elif self.class_scope_table.has_key(name):
            value = self.class_scope_table[name]
            return value[INDEX_POS]
        return NONE

