import unittest
from math import isclose


from lexer import (
    Lexer,
    LexerError,
    EmptyInputException,
)

from tokens import (
    Token,
    TokenType,
)

from ast import (
    BinOpNode,
    UnOpNode,
)

from parser import (
    Parser,
)

from evaluators import (
    Interpreter,
    Sexp,
    VM,
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


class PlusOneSexpTest(unittest.TestCase):
    def test_sexp_basic(self):
        code = '1+2'
        lexer = Lexer(code)
        parser = Parser(lexer)
        ast = parser.parse()
        sexp = Sexp(ast).to_sexp()
        self.assertEqual(
            sexp,
            ['+', 1, 2]
        )

    def test_sexp_more_featured(self):
        code = '1+2/(-42)*3'
        lexer = Lexer(code)
        parser = Parser(lexer)
        ast = parser.parse()
        sexp = Sexp(ast).to_sexp()
        self.assertEqual(
            sexp,
            ['+', 1, ['*', ['/', 2, ['-', 42]], 3]]
        )


class PlusOneInterpreterTest(unittest.TestCase):
    def test_interpreter_basic(self):
        code = '1+2/(-42)*3'
        lexer = Lexer(code)
        parser = Parser(lexer)
        ast = parser.parse()
        result = Interpreter(ast).interpret()
        self.assertTrue(isclose(result, 0.8571428571))


class PlusOneVMTest(unittest.TestCase):
    def test_vm_basic(self):
        code = '1+2/(-42)*3'
        lexer = Lexer(code)
        parser = Parser(lexer)
        ast = parser.parse()
        vm = VM(ast)
        result = vm.run()
        self.assertEqual(vm.operator_stack, [])
        self.assertEqual(vm.operands_stack, [])
        self.assertTrue(result, 16)

if __name__ == '__main__':
    unittest.main()
