from tokens import (
    ONE_CHAR_TOKENS_MAPPING,
    Token,
    TokenType,
)


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
