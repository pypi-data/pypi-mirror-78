from enum import Enum, auto

from .graph import Out, OutDim
from .node import NodeLetType


def is_estimable(value):
    if isinstance(value, (Variable, Expr)):
        return value.is_estimable()
    return value is not None


def is_hint(value):
    if isinstance(value, (Variable, Expr)):
        return value.is_hint()
    return isinstance(value, Out)


def clone_value(value, variables):
    if isinstance(value, (Variable, Expr)):
        return value.clone(variables)
    if isinstance(value, dict):
        return {k: clone_value(v, variables) for k, v in value.items()}
    if isinstance(value, list):
        return [clone_value(v, variables) for v in value]
    if isinstance(value, Shape):
        return Shape(clone_value(value.dims, variables), value.name)
    if isinstance(value, (bool, int, float, str, OutDim)) or value is None:
        return value
    raise Exception('unreachable code')


def repr_value(value):
    if isinstance(value, bool):
        return 'yes' if value else 'no'
    return repr(value)


class Variable:
    def __init__(self, name, value=None):
        super().__init__()
        self.id = None
        self.id_old = None
        self.name = name
        self.shortcut = None
        self.ty = None
        self.value = value

    def detach(self, id):
        cloned = Variable(self.name, self.value)
        cloned.id = id
        cloned.id_old = self.id
        cloned.shortcut = self.shortcut
        cloned.ty = self.ty
        return cloned

    def clone(self, variables):
        for var in variables:
            if var.name == self.name and var.id_old == self.id:
                return var
        return self

    def assert_estimable(self):
        assert is_estimable(self.value), f'unestimable variable: {self.name}'
        return True

    def is_estimable(self):
        return is_estimable(self.value)

    def is_hint(self):
        return self.ty == NodeLetType.DIM or is_hint(self.value)

    def __repr__(self):
        if self.value is not None:
            return f'{self.name}={repr_value(self.value)}'
        return self.name


class Operator(Enum):
    NEG = auto()
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()
    POW = auto()
    AND = auto()
    OR = auto()
    XOR = auto()

    def __repr__(self):
        if self == self.NEG:
            return '-'
        if self == self.ADD:
            return '+'
        if self == self.SUB:
            return '-'
        if self == self.MUL:
            return '*'
        if self == self.DIV:
            return '/'
        if self == self.MOD:
            return '%'
        if self == self.POW:
            return '**'
        if self == self.AND:
            return '&'
        if self == self.OR:
            return '|'
        if self == self.XOR:
            return '^'


OperatorFn = {
    Operator.NEG: lambda a, _: -a,
    Operator.ADD: lambda a, b: a + b,
    Operator.SUB: lambda a, b: a - b,
    Operator.MUL: lambda a, b: a * b,
    Operator.DIV: lambda a, b: a / b,
    Operator.MOD: lambda a, b: a % b,
    Operator.POW: lambda a, b: a ** b,
    Operator.AND: lambda a, b: a & b,
    Operator.OR: lambda a, b: a | b,
    Operator.XOR: lambda a, b: a ^ b,
}


class Expr:
    def __init__(self, op, lhs, rhs=None):
        super().__init__()
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def clone(self, variables):
        lhs = clone_value(self.lhs, variables)
        rhs = clone_value(self.rhs, variables)
        return Expr(self.op, lhs, rhs)

    def is_estimable(self):
        is_estimable(self.lhs)
        if self.rhs:
            is_estimable(self.rhs)
        return True

    def is_hint(self):
        return is_hint(self.lhs) or is_hint(self.rhs)

    def __repr__(self):
        if self.rhs is None:
            return f'{repr(self.op)}{repr_value(self.lhs)}'
        return f'({repr_value(self.lhs)} {repr(self.op)} {repr_value(self.rhs)})'


class Shape:
    def __init__(self, dims, name='x'):
        super().__init__()
        self.name = name
        self.dims = dims

    def add(self):
        value = 0
        for dim in self.dims or []:
            value = Expr(Operator.ADD, value, dim)
        return value

    def product(self):
        value = 1
        for dim in self.dims or []:
            value = Expr(Operator.MUL, value, dim)
        return value

    def __len__(self):
        return len(self.dims)

    def __repr__(self):
        dims = ', '.join(repr_value(d) if d else '*' for d in self.dims)
        return f' = {dims}'
