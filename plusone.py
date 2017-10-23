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

    def number(self):
        result = []
        while self.current_char is not None and self.current_char.isdigit():
            result.append(self.current_char)
            self.advance()

        if self.current_char == '.':
            result.append('.')
            self.advance()
        else:
            return int(''.join(result))

        while self.current_char is not None and self.current_char.isdigit():
            result.append(self.current_char)
            self.advance()

        return float(''.join(result))

    def one_char(self):
        result = ONE_CHAR_TOKENS_MAPPING[self.current_char]
        self.advance()
        return result

    def error(self, message):
        raise LexerError(message)

    def next_token(self):
        if self.current_char is None:
            return Token(TokenType.EOF, None)

        if self.current_char.isspace():
                self.whitespaces()

        if self.current_char is None:
            return Token(TokenType.EOF, None)

        if self.current_char.isdigit():
            number = self.number()
            if type(number) is float:
                token_type = TokenType.FLOAT
            else:
                token_type = TokenType.INTEGER
            return Token(token_type, number)

        if self.current_char in ONE_CHAR_TOKENS_MAPPING.keys():
            current_char = self.current_char
            return Token(self.one_char(), current_char)

        self.error('Unexpected char:{}'.format(self.current_char))

    def all_tokens(self):
        tokens = []
        while True:
            token = self.next_token()
            if token.type == TokenType.EOF:
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
        return 'BinOpNode({}, {}, {})'.format(
            self.lhs.__class__,
            self.op,
            self.rhs.__class__,
        )

    def __eq__(self, other):
        if self.lhs == other.lhs and \
                self.op == other.op and \
                self.rhs == other.rhs:
            return True
        return False


class UnOpNode(AST):
    def __init__(self, op, value):
        self.op = op
        self.value = value

    def __repr__(self):
        return 'UnOpNode({}, {})'.format(self.op, self.value.__class__)

    def __eq__(self, other):
        if self.value == other.value and \
                self.op == other.op:
            return True
        return False


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
            current_token = self.current_token
            self.eat(self.current_token.type)
            return UnOpNode(current_token, self.expr())

    def parse(self):
        self.current_token = self.lexer.next_token()
        return self.expr()
        if self.current_token != Token(TokenType.EOF, None):
            self.error()


class Sexp:
    def __init__(self, ast):
        self.ast = ast

    def to_sexp(self):
        return self.to_sexp_helper(self.ast)

    def to_sexp_helper(self, node):
        if isinstance(node, BinOpNode):
            return [
                node.op.value,
                self.to_sexp_helper(node.lhs),
                self.to_sexp_helper(node.rhs),
            ]
        elif isinstance(node, UnOpNode):
            return [
                node.op.value,
                self.to_sexp_helper(node.value),
            ]
        elif isinstance(node, Token):
            return node.value
        else:
            raise Error('Node could not be recognised')


class Visitor:
    def visit(self, node):
        klass_name = type(node).__name__
        visitor = getattr(self, 'visit_{}'.format(klass_name))
        return visitor(node)


class Interpreter(Visitor):
    def __init__(self, ast):
        self.ast = ast

    def interpret(self):
        return self.visit(self.ast)

    def visit_BinOpNode(self, node):
        left = self.visit(node.lhs)
        right = self.visit(node.rhs)
        op = node.op

        if op.type == TokenType.ADD:
            return left + right
        elif op.type == TokenType.MINUS:
            return left - right
        elif op.type == TokenType.MULT:
            return left * right
        elif op.type == TokenType.DIV:
            return left / right

    def visit_UnOpNode(self, node):
        value = self.visit(node.value)
        op = node.op

        if op.type == TokenType.ADD:
            return value
        elif op.type == TokenType.MINUS:
            return -value

    def visit_Token(self, node):
        return node.value


if __name__ == '__main__':
    import pprint

    code = '12+2*4-2000+323-3/24*(-2)'
    tokens = Lexer(code)
    ast = Parser(Lexer(code)).parse()
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(Sexp(ast).to_sexp())
    print(Interpreter(ast).interpret())
