class Out:
    def __init__(self, id=None, name=None):
        super().__init__()
        self.id = id
        self.name = name

    def __eq__(self, other):
        return isinstance(other, type(self)) and (self.id, self.name) == (other.id, other.name)

    def __hash__(self):
        return hash((self.id, self.name))

    def __repr__(self):
        id = self.id if self.id is not None else ''
        name = self.name or ''
        return f'{name}${id}'


class OutDim:
    def __init__(self, out, dim):
        super().__init__()
        self.out = out
        self.dim = dim


class NodeArg:
    def __init__(self, name, value):
        super().__init__()
        self.name = name
        self.value = value

    def __repr__(self):
        return f'{self.name}={self.value}'


class NodeCall:
    def __init__(self, name, inputs, args):
        super().__init__()
        self.name = name
        self.inputs = inputs
        self.args = args

    def get_arg(self, name):
        assert self.args is not None, f'unexpected empty args: {self.name}'

        assert name in self.args.keys(
        ), f'no such variable: {name} in {self.name}'

        return self.args[name]

    def __repr__(self):
        if isinstance(self.inputs, list):
            inputs = '[' + ', '.join(str(i) for i in self.inputs) + ']'
        elif isinstance(self.inputs, dict):
            if len(self.inputs) == 1 and 'x' in self.inputs.keys():
                inputs = ''
            else:
                inputs = '{' + ', '.join(f'{k}={str(i)}'
                                         for k, i in self.inputs.items()) + '}'
        else:
            inputs = ''

        if self.args:
            args = '(' + ', '.join(str(a) for a in self.args.values()) + ')'
        else:
            args = ''

        return self.name + inputs + args


class GraphNode:
    def __init__(self, id, calls, shapes):
        super().__init__()
        self.id = id
        self.calls = calls
        self.shapes = shapes

        self._depth = 1

    def increse_depth(self):
        self._depth += 1

    def __repr__(self):
        indent = ' ' * (4 * self._depth)
        calls = ' + '.join(str(c) for c in self.calls)

        if not self.shapes:
            shapes = ''
        elif len(self.shapes) == 1 and 'x' in self.shapes.keys():
            shapes = str(self.shapes['x'])
        else:
            indent_shapes = indent + ' ' * 4
            shapes = ':\n' + '\n'.join(indent_shapes + k + str(s)
                                       for k, s in self.shapes.items())

        return f'{indent}{self.id}. {calls}{shapes}'
