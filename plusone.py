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
    def __init__(self, type, value=''):
        self.type = type
        self.value = value

    def __repr__(self):
        return 'Token({}, {})'.format(self.type, self.value)

    def __eq__(self, other):
        if self.type == other.type and self.value == other.value:
            return True
        return False


class EmptyInputException(Exception):
    pass


class LexerError(Exception):
    pass


class Lexer:
    def __init__(self, text):
        if len(text) == 0:
            raise EmptyInputException

        self.pos = 0
        self.text = text
        self.current_char = self.text[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def whitespaces(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def digit(self):
        result = []
        while self.current_char is not None and self.current_char.isdigit():
            result.append(self.current_char)
            self.advance()
        return int(''.join(result))

    def one_char(self):
        result = ONE_CHAR_TOKENS_MAPPING[self.current_char]
        self.advance()
        return result

    def error(self, message):
        raise LexerError(message)

    def next_token(self):
        if self.current_char is None:
            return Token(TokenType.EOF)

        if self.current_char.isspace():
                self.whitespaces()

        if self.current_char is None:
            return Token(TokenType.EOF)

        if self.current_char.isdigit():
            return Token(TokenType.INTEGER, self.digit())

        if self.current_char in ONE_CHAR_TOKENS_MAPPING.keys():
            return Token(self.one_char())

        self.error('Unexpected char:{}'.format(self.current_char))

    def all_tokens(self):
        tokens = []
        while True:
            token = self.next_token()
            if token == Token(TokenType.EOF):
                return tokens
            tokens.append(token)


class AST:
    pass


class BinOpNode(AST):
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def __repr__(self):
        return 'BinOpNode({}, {}, {})'.format(self.lhs, self.op, self.rhs)


class UnOpNode(AST):
    def __init__(self, op, value):
        self.op = op
        self.value = value

    def __repr__(self):
        return 'UnOpNode({}, {})'.format(self.op, self.value)


class ParserError(Exception):
    pass


class Parser:
    '''
    expr: term ([+-] term)*
    term: factor ([*/] factor)*
    factor: INTEGER
        | ( expr )
        | [+-] expr
    '''
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None

    def eat(self, type):
        if self.current_token.type == type:
            self.current_token = self.lexer.next_token()
        else:
            raise ParserError(
                    'Expecting {}, got {}'.format(
                        self.current_token.type,
                        type,
                    )
            )

    def expr(self):
        lhs = self.term()
        while self.current_token.type in (TokenType.ADD, TokenType.MINUS):
            op = self.current_token
            self.eat(self.current_token.type)
            rhs = self.term()
            lhs = BinOpNode(lhs, op, rhs)
        return lhs

    def term(self):
        lhs = self.factor()
        while self.current_token.type in (TokenType.MULT, TokenType.DIV):
            op = self.current_token
            self.eat(self.current_token.type)
            rhs = self.factor()
            lhs = BinOpNode(lhs, op, rhs)
        return lhs

    def factor(self):
        if self.current_token.type == TokenType.INTEGER:
            token = self.current_token
            self.eat(TokenType.INTEGER)
            return token
        elif self.current_token.type == TokenType.L_PAREN:
            self.eat(TokenType.L_PAREN)
            token = self.expr()
            self.eat(TokenType.R_PAREN)
            return token
        elif self.current_token.type in (TokenType.ADD, TokenType.MINUS):
            self.eat(self.current_token.type)
            return UnOpNode(self.current_token, self.expr())

    def parse(self):
        self.current_token = self.lexer.next_token()
        return self.expr()
        if self.current_token != Token(TokenType.EOF):
            self.error()

if __name__ == '__main__':
    code = '12*2+4'
    tokens = Lexer(code)
    print(tokens.all_tokens())
    ast = Parser(Lexer(code)).parse()
    print(ast)
