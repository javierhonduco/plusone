from tokens import TokenType

from ast import (
    BinOpNode,
    UnOpNode,
)


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
