# Many of this code is from:
# https://github.com/lark-parser/lark/blob/master/examples/python_parser.py

from lark import Lark, Transformer
from lark.indenter import Indenter

from .. import ast


class _Indenter(Indenter):
    NL_type = '_NEWLINE'
    OPEN_PAREN_types = ['LPAR', 'LSQB', 'LBRACE']
    CLOSE_PAREN_types = ['RPAR', 'RSQB', 'RBRACE']
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 8


class _Transformer(Transformer):
    _USE_TYPES = {
        'use_by_local': ast.UseByLocal,
        'use_by_author': ast.UseByAuthor,
        'use_by_web': ast.UseByWeb,
    }

    _OPS = {
        '+': ast.Operator.ADD,
        '-': ast.Operator.SUB,
        '*': ast.Operator.MUL,
        '/': ast.Operator.DIV,
        '%': ast.Operator.MOD,
    }

    def file_input(self, args):
        return ast.File(args[:-1], args[-1])

    def rootdef(self, args):
        args[1].ty = args[0]
        return args[1]

    def node_type_extern(self, args):
        return ast.NodeType.EXTERN

    def node_type_data(self, args):
        return ast.NodeType.DATA

    def node_type_optim(self, args):
        return ast.NodeType.OPTIM

    def node_type_exec(self, args):
        return ast.NodeType.EXEC

    def node_type_default(self, args):
        return ast.NodeType.DEFAULT

    def use(self, args):
        name = str(args[0])
        by = args[1]
        by_method = by.data
        by_source = str(by.children[0]) if by.data != 'use_by_local' else None
        return self._USE_TYPES[by_method](name, by_source)

    def nodedef(self, args):
        return ast.Node(str(args[0]), *args[1:])

    def node_suite_let(self, args):
        # TODO: check duplicated names
        return {a.name: a for a in args}

    def node_suite_with(self, args):
        # TODO: check duplicated names
        return {a.name: a for a in args}

    def node_suite_children(self, args):
        # TODO: check duplicated names
        return {a.name: a for a in args}

    def node_suite_graph(self, args):
        # TODO: check duplicated names
        return {a.id: a for a in args}

    def nodelet(self, args):
        name = str(args[1])
        shortcut = str(args[0]) if args[0] is not None else None
        ty, value = args[2]
        return ast.NodeLet(name, shortcut, ty, value)

    def nodelet_type_bool(self, args):
        return ast.NodeLetType.BOOL, args[0] if args else None

    def nodelet_type_int(self, args):
        return ast.NodeLetType.INT, args[0] if args else None

    def nodelet_type_real(self, args):
        return ast.NodeLetType.REAL, args[0] if args else None

    def nodelet_type_data(self, args):
        return ast.NodeLetType.DATA, str(args[0]) if args else None

    def nodelet_type_optim(self, args):
        return ast.NodeLetType.OPTIM, str(args[0]) if args else None

    def nodelet_type_node(self, args):
        return ast.NodeLetType.NODE, str(args[0]) if args else None

    def nodelet_type_dim(self, args):
        return ast.NodeLetType.DIM, None

    def graph(self, args):
        return ast.GraphNode(args[0], args[1], args[2] if len(args) > 2 else None)

    def graph_nodes(self, args):
        return args

    def graph_node(self, args):
        return ast.NodeCall(str(args[0]), args[1], args[2])

    def graph_inputs_dict(self, args):
        # TODO: check duplicated names
        return {a[0]: a[1] for a in args}

    def graph_inputs_list(self, args):
        return args

    def graph_input_kw(self, args):
        return str(args[0]), args[1]

    def graph_args(self, args):
        # TODO: check duplicated names
        return {a.name: a for a in args}

    def graph_arg(self, args):
        return ast.NodeArg(str(args[0]), args[1])

    def graph_shapes(self, args):
        # TODO: check duplicated names
        return {a.name: a for a in args}

    def graph_shape_kw(self, args):
        args[1].name = str(args[0])
        return args[1]

    def graph_shape(self, args):
        return ast.Shape(args)

    def dim(self, args):
        return args[0] if args else None

    def out(self, args):
        return ast.Out(args[1], str(args[0] or 'x'))

    def out_const(self, args):
        return args[0]

    def withdef(self, args):
        return ast.With(str(args[0]), args[1])

    def with_suite(self, args):
        # TODO: check duplicated names
        return {a.name: a for a in args}

    def withset(self, args):
        return ast.WithSet(args[0], args[1])

    def expr(self, args):
        return ast.Expr(ast.Operator.OR, args[0], args[1])

    def xor_expr(self, args):
        return ast.Expr(ast.Operator.XOR, args[0], args[1])

    def and_expr(self, args):
        return ast.Expr(ast.Operator.AND, args[0], args[1])

    def arith_expr(self, args):
        return ast.Expr(self._OPS[args[1]], args[0], args[2])

    def term(self, args):
        return ast.Expr(self._OPS[args[1]], args[0], args[2])

    def factor(self, args):
        return ast.Expr(ast.Operator.NEG, args[1])

    def power(self, args):
        return ast.Expr(ast.Operator.POW, args[0], args[1])

    def variable(self, args):
        return ast.Variable(str(args[0]))

    def fullname(self, args):
        return ' '.join(args)

    def BOOL_YES(self, _):
        return True

    def BOOL_NO(self, _):
        return False

    def DEC_NUMBER(self, value):
        return int(value)

    def FLOAT_NUMBER(self, value):
        return float(value)


class Parser:
    def __init__(self):
        super().__init__()
        self._inner = Lark.open(
            'grammar.lark',
            parser='lalr',
            rel_to=__file__,
            postlex=_Indenter(),
            start='file_input',
            maybe_placeholders=True,
            cache=True,
        )
        self._transformer = _Transformer()

    def parse(self, source: str):
        tree = self._inner.parse(source + '\n')
        return self._transformer.transform(tree)
