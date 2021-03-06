from tokens import (
    Token,
    TokenType,
)

from ast import (
    BinOpNode,
    UnOpNode,
)


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


class VM(Visitor):
    def __init__(self, ast):
        self.ast = ast
        self.stack = []
        self.operator_stack = []
        self.operands_stack = []

    def run(self):
        self.do_visit()
        return self.do_interpret()

    def do_visit(self):
        self.visit(self.ast)

    def create_stacks(self):
        for element in self.stack:
            if isinstance(element, UnOpNode) or isinstance(element, BinOpNode):
                self.operator_stack.append(element)
            else:
                self.operands_stack.append(element)

    def interpret_binop(self, op):
        left = self.operands_stack.pop(0)
        right = self.operands_stack.pop(0)

        if op.type == TokenType.ADD:
            result = left + right
        elif op.type == TokenType.MINUS:
            result = left - right
        elif op.type == TokenType.MULT:
            result = left * right
        elif op.type == TokenType.DIV:
            result = left / right

        return result

    def interpret_unop(self, op):
        expr = self.operands_stack.pop(0)
        if op.type == TokenType.ADD:
            result = +expr  # unnecessary, but well...
        elif op.type == TokenType.MINUS:
            result = -expr
        return result

    def interpret_node(self, node):
        if isinstance(node, BinOpNode):
            return self.interpret_binop(node.op)
        elif isinstance(node, UnOpNode):
            return self.interpret_unop(node.op)

    def do_interpret(self):
        self.create_stacks()

        while self.operator_stack:
            node = self.operator_stack.pop(0)
            result = self.interpret_node(node)
            self.operands_stack.insert(0, result)

        return self.operands_stack.pop()

    def visit_BinOpNode(self, node):
        left = self.visit(node.lhs)
        right = self.visit(node.rhs)

        self.stack.extend(filter(None, [left, right, node]))

    def visit_UnOpNode(self, node):
        value = self.visit(node.value)

        self.stack.extend([value, node])

    def visit_Token(self, node):
        return node.value
