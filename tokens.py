from enum import Enum


class TokenType(Enum):
    EOF = 0
    INTEGER = 1
    FLOAT = 2
    L_PAREN = 3
    R_PAREN = 4
    ADD = 5
    MINUS = 6
    MULT = 7
    DIV = 8


ONE_CHAR_TOKENS_MAPPING = {
    '(': TokenType.L_PAREN,
    ')': TokenType.R_PAREN,
    '+': TokenType.ADD,
    '-': TokenType.MINUS,
    '*': TokenType.MULT,
    '/': TokenType.DIV,
}


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return 'Token({}, {})'.format(self.type, self.value)

    def __eq__(self, other):
        if self.type == other.type and self.value == other.value:
            return True
        return False
