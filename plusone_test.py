import unittest

from plusone import (
    BinOpNode,
    EmptyInputException,
    Lexer,
    LexerError,
    Parser,
    Token,
    TokenType,
    UnOpNode,
)


class PlusOneLexerTest(unittest.TestCase):
    def test_handle_spaces(self):
        expected_tokens = [
            Token(TokenType.INTEGER, 314),
            Token(TokenType.ADD, '+'),
            Token(TokenType.INTEGER, 42),
        ]
        code = ' 314      + 42 '
        tokens = Lexer(code).all_tokens()
        self.assertEqual(tokens, expected_tokens)

    def test_basic_lexer(self):
        expected_tokens = [
            Token(TokenType.INTEGER, 314),
            Token(TokenType.ADD, '+'),
            Token(TokenType.INTEGER, 42),
            Token(TokenType.MULT, '*'),
            Token(TokenType.L_PAREN, '('),
            Token(TokenType.INTEGER, 1),
            Token(TokenType.DIV, '/'),
            Token(TokenType.INTEGER, 2),
            Token(TokenType.R_PAREN, ')'),
        ]
        code = '314+42*(1/2)'
        tokens = Lexer(code).all_tokens()
        self.assertEqual(tokens, expected_tokens)

    def test_basic_lexer_floats(self):
        expected_tokens = [
            Token(TokenType.INTEGER, 42),
            Token(TokenType.ADD, '+'),
            Token(TokenType.FLOAT, 3.14),
        ]
        code = '42+3.14'
        tokens = Lexer(code).all_tokens()
        self.assertEqual(tokens, expected_tokens)

    def test_empty_code(self):
        code = ''
        with self.assertRaises(EmptyInputException):
            Lexer(code).all_tokens()

    def test_lexer_error(self):
        code = '\\'
        with self.assertRaises(LexerError):
            Lexer(code).all_tokens()


class PlusOneParserTest(unittest.TestCase):
    def test_parser_basic(self):
        code = '1+2'
        lexer = Lexer(code)
        parser = Parser(lexer)
        ast = parser.parse()
        self.assertEqual(
            ast,
            BinOpNode(
                Token(TokenType.INTEGER, 1),
                Token(TokenType.ADD, '+'),
                Token(TokenType.INTEGER, 2),
            ),
        )

    def test_parser_basic_with_unary(self):
        code = '1+2-(-1)'
        lexer = Lexer(code)
        parser = Parser(lexer)
        ast = parser.parse()
        self.assertEqual(
            ast,
            BinOpNode(
                BinOpNode(
                    Token(TokenType.INTEGER, 1),
                    Token(TokenType.ADD, '+'),
                    Token(TokenType.INTEGER, 2),
                ),
                Token(TokenType.MINUS, '-'),
                UnOpNode(
                    Token(TokenType.MINUS, '-'),
                    Token(TokenType.INTEGER, 1),
                ),
            ),
        )

    def test_operator_precedance_mult_left(self):
        code = '1*2+3'
        lexer = Lexer(code)
        parser = Parser(lexer)
        ast = parser.parse()
        self.assertEqual(
            ast,
            BinOpNode(
                BinOpNode(
                    Token(TokenType.INTEGER, 1),
                    Token(TokenType.MULT, '*'),
                    Token(TokenType.INTEGER, 2),
                ),
                Token(TokenType.ADD, '+'),
                Token(TokenType.INTEGER, 3),
            ),
        )

    def test_operator_precedance_mult_right(self):
        code = '1+2*3'
        lexer = Lexer(code)
        parser = Parser(lexer)
        ast = parser.parse()
        self.assertEqual(
            ast,
            BinOpNode(
                Token(TokenType.INTEGER, 1),
                Token(TokenType.ADD, '+'),
                BinOpNode(
                    Token(TokenType.INTEGER, 2),
                    Token(TokenType.MULT, '*'),
                    Token(TokenType.INTEGER, 3),
                ),
            ),
        )

    def test_operator_precedance_mult_force_right(self):
        code = '1*(2+3) '
        lexer = Lexer(code)
        parser = Parser(lexer)
        ast = parser.parse()
        self.assertEqual(
            ast,
            BinOpNode(
                Token(TokenType.INTEGER, 1),
                Token(TokenType.MULT, '*'),
                BinOpNode(
                    Token(TokenType.INTEGER, 2),
                    Token(TokenType.ADD, '+'),
                    Token(TokenType.INTEGER, 3),
                ),
            ),
        )


if __name__ == '__main__':
    unittest.main()
