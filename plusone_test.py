import unittest

from plusone import Token, TokenType, Lexer, EmptyInputException, LexerError


class PlusOneTest(unittest.TestCase):
    def test_handle_spaces(self):
        expected_tokens = [
            Token(TokenType.INTEGER, 314),
            Token(TokenType.ADD),
            Token(TokenType.INTEGER, 42),
        ]
        code = ' 314      + 42 '
        tokens = Lexer(code).all_tokens()
        self.assertEqual(tokens, expected_tokens)

    def test_basic_lexer(self):
        expected_tokens = [
            Token(TokenType.INTEGER, 314),
            Token(TokenType.ADD),
            Token(TokenType.INTEGER, 42),
            Token(TokenType.MULT),
            Token(TokenType.L_PAREN),
            Token(TokenType.INTEGER, 1),
            Token(TokenType.DIV),
            Token(TokenType.INTEGER, 2),
            Token(TokenType.R_PAREN),
        ]
        code = '314+42*(1/2)'
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

if __name__ == '__main__':
    unittest.main()
