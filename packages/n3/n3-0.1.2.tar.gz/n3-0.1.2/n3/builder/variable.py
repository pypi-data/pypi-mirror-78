from .. import ast


def replace(names, value, variables, shortcuts):
    if value is None:
        return None
    elif isinstance(value, ast.Variable):
        if value.name in names:
            names = ', '.join(reversed(names))
            raise Exception(f'cycled variable: {names}')
        if value.name in shortcuts.keys():
            value.name = shortcuts[value.name]
        if value.name in variables.keys():
            value = variables[value.name]

        names.append(value.name)
        value.value = replace(names, value.value, variables, shortcuts)
        names.pop()
        return value
    elif isinstance(value, ast.Expr):
        value.lhs = replace(names, value.lhs, variables, shortcuts)
        value.rhs = replace(names, value.rhs, variables, shortcuts)
    return value


def build(value):
    if isinstance(value, ast.Variable):
        if value.is_hint():
            return value
        if value.value is None:
            raise Exception(f'value is needed: {value.name}')
        return ast.TypeConverter[value.ty](build(value.value))
    if isinstance(value, ast.Expr):
        lhs = build(value.lhs)
        rhs = build(value.rhs)
        if ast.is_hint(lhs) or ast.is_hint(rhs):
            return ast.Expr(value.op, lhs, rhs)
        return ast.OperatorFn[value.op](lhs, rhs)
    if isinstance(value, list):
        return [build(v) for v in value]
    if isinstance(value, dict):
        return {k: build(v) for k, v in value.items()}
    if isinstance(value, ast.Shape):
        dims = [int(v) for v in build(value.dims)]
        return ast.Shape(dims, value.name)
    return value


class Graph:
    def __init__(self, id):
        super().__init__()
        self._id = id
        self._shortcuts = {}
        self._variables = {}

    def clone(self, id, variables):
        # Step 1. get the copies
        self_variables = {k: v.detach(id) for k, v in self._variables.items()}
        self_shortcuts = {v.shortcut or v.name: v
                          for name, v in self_variables.items()}

        variables += list(self_variables.values())

        # Step 2. replace the olds into the news
        for var in self_variables.values():
            var.value = ast.clone_value(var.value, variables)

        # Step 3. store
        graph = Graph(id)
        graph._shortcuts = self_shortcuts
        graph._variables = self_variables
        return graph

    def add(self, variable):
        if variable.name in self._variables.keys():
            raise Exception(f'duplicated variable: {variable.name}')
        variable.id = variable.id_old = self._id
        self._variables[variable.name] = variable

    def get(self, name):
        return self._variables[name]

    def build(self):
        shortcuts_map = {v.shortcut: name
                         for name, v in self._variables.items()
                         if v.shortcut}
        self._variables = {name: replace([], v, self._variables, shortcuts_map)
                           for name, v in self._variables.items()}
        self._shortcuts = {v.shortcut or v.name: v
                           for v in self._variables.values()}

    def hint(self, out, dims):
        def _hint(out, dim, value, is_root=False):
            if isinstance(value, ast.Variable):
                if value.name not in self._shortcuts.keys():
                    candidates = ', '.join(self._shortcuts.keys())
                    raise Exception(
                        f'no such variable: {value.name}, candidates are: {candidates}')
                output = self._shortcuts[value.name]
                # hint in-place
                if output.ty == ast.NodeLetType.DIM and is_root:
                    output.value = ast.OutDim(out, dim)
                return output
            if isinstance(value, ast.Expr):
                value.lhs = _hint(out, dim, value.lhs)
                value.rhs = _hint(out, dim, value.rhs)
            return value

        return [_hint(out, dim, v, is_root=True) for dim, v in enumerate(dims)]

    def replace(self, value):
        if value is None:
            return None
        elif isinstance(value, ast.Variable):
            if value.name in self._shortcuts.keys():
                return self._shortcuts[value.name]
            raise Exception(f'no such variable: {value.name}')
        elif isinstance(value, ast.Expr):
            value.lhs = self.replace(value.lhs)
            value.rhs = self.replace(value.rhs)
        return value

    def apply(self, variables, is_shortcut=False):
        # TODO: test types
        self_variables = self._shortcuts if is_shortcut else self._variables
        for k, v in variables.items():
            self_variables[k].value = v

    def assert_estimable(self):
        all(v.assert_estimable() for v in self._variables.values())

    def get_variables(self):
        return self._variables

    def __repr__(self):
        return '\n'.join(f'let {v}' for v in self._variables.values())
