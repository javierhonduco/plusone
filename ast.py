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
