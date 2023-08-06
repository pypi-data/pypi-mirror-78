from copy import copy
import importlib.util

import torch.nn as nn

from .. import ast, std
from ..parser import Parser
from ..util import EnvVars
from .extern_node import DataNode, ExternNode, NodeExecutable, OptimNode
from .tensor import TensorGraph
from .variable import Graph
from .variable import build as build_variable


_BuiltinsInput = ['AssertShape', ]
_BuiltinsNode = ['Transform', 'Concat', ]


def make_graph(id, variables):
    graph = Graph(id)
    for let in variables.values():
        var = ast.Variable(let.name, let.value)
        var.shortcut = let.shortcut
        var.ty = let.ty
        graph.add(var)
    graph.build()
    return graph


def _assert_tensor_graph_name(node: ast.GraphNode, expects,
                              inputs=None, args=False, sized=False):
    expects = ' | '.join(expects)

    num_calls = len(node.calls)
    assert num_calls == 1, f'Expected {expects} node, Given {num_calls} nodes'
    call = node.calls[0]
    assert call.name in expects, f'Expected {expects} node, Given {call.name}'

    if inputs is None:
        assert call.inputs is None, f'unexpected inputs: {call.name}'
    elif inputs is list:
        type_name = inputs.__name__
        assert isinstance(
            call.inputs, inputs), f'Expected {inputs.__name__} inputs, Given {type_name}'

    if not args:
        assert call.args is None, f'Expected {expects} node, Given {repr(call)}'
    if sized:
        assert node.shapes is not None, f'Expected sized node: {call.name}'
    return call


def _merge_shapes(last_outputs, new_inputs):
    for name in last_outputs.keys():
        last_output = last_outputs[name]
        new_input = new_inputs[name]

        # dynamic size
        if not new_input:
            new_inputs[name] = last_output
            continue

        assert len(last_output) == len(new_input), \
            f'Expected {len(new_input)} dims, Given {len(last_output)} dims'

        for dim in range(len(new_input)):
            last_dim = last_output.dims[dim]
            new_dim = new_input.dims[dim]
            if not ast.is_hint(last_dim):
                # replace
                if ast.is_hint(new_dim):
                    new_dim.ty = ast.NodeLetType.INT
                    new_dim.value = last_dim
                # test value
                elif ast.is_estimable(last_dim) and ast.is_estimable(new_dim):
                    last_dim = build_variable(last_dim)
                    new_dim = build_variable(new_dim)
                    assert last_dim == new_dim, f'Expected {new_dim}, Given {last_dim}'


class NodeIR:
    def __init__(self, name, graph, tensor_graph):
        super().__init__()
        self.name = name
        self.graph = graph
        self.tensor_graph = tensor_graph

        self.id = None
        self.input = None
        self.output = None

    def clone(self, root, variables):
        graph = self.graph.clone(root.generate_id(), variables)
        tensor_graph = [n.clone(root, variables) for n in self.tensor_graph]

        cloned = NodeIR(self.name, graph, tensor_graph)
        cloned.id = self.id
        cloned.input = copy(self.input)
        cloned.output = copy(self.output)
        return cloned

    def get_input_shapes(self):
        input_node = self.tensor_graph[0]
        if input_node.name in _BuiltinsInput:
            return input_node.get_output_shapes()
        return input_node.get_input_shapes()

    def get_output_shapes(self):
        for output_node in reversed(self.tensor_graph):
            shapes = output_node.get_output_shapes()
            if shapes:
                # filter dynamic size
                if len(shapes) == 1 and 'x' in shapes.keys():
                    if not shapes['x']:
                        continue
                return shapes
        return self.tensor_graph[-1].get_output_shapes()

    def apply_variables(self, variables, is_shortcut=False):
        self.graph.apply(variables, is_shortcut=is_shortcut)

    def build(self, root):
        input = self.input or {k: ast.Out(0, k)
                               for k in self.get_input_shapes().keys()}
        output = self.output or {k: ast.Out(1, k)
                                 for k in self.get_output_shapes().keys()}
        tensor_graph = [n.build(root) for n in self.tensor_graph]
        if len(tensor_graph) == 1:
            node = tensor_graph[0]
            if isinstance(node, (DataNode, OptimNode)):
                return tensor_graph[0]
        return NodeExecutable(self.name, input, output, tensor_graph)

    def __repr__(self):
        name = f'[node ir {self.name}]'
        graph = repr(self.graph)
        tensor_graph = '\n'.join(f'({id}) {repr(n)}'
                                 for id, n in enumerate(self.tensor_graph))
        return f'{name}\n{graph}\n\n{tensor_graph}'


class NodeContainer:
    def __init__(self, parent, name):
        super().__init__()
        self.parent = parent
        self.name = name

        self.graph = None
        self.tensor_graph = []

        self.children = {}

        self.last_id = 0

    @property
    def root(self):
        if isinstance(self.parent, NodeRoot):
            return self.parent
        return self.parent.root

    def add_use(self, use: ast.Use):
        # Step 1. get the source
        # Step 2. build
        # Step 3. store
        raise NotImplementedError()

    def add_with(self, w: ast.With):
        # Step 1. get the node
        node = self.get(w.name)

        # Step 2. apply variables
        args = {k: self.graph.replace(v.value)
                for k, v in w.variables.items()}
        node.apply_variables(args)

        # Step 3. store
        self.children[w.name] = node

    def add_child(self, child: ast.Node):
        # Step 1. convert to file
        file = ast.File([], child)

        # Step 2. build
        node = self._build(file, self)

        # Step 3. store
        self.children[child.name] = node

    def add_tensor_graph(self, node: ast.GraphNode):
        # input node
        if node.id == 0:
            call = _assert_tensor_graph_name(node, ['Input'], sized=True)

            output = {s: ast.Out(0, s) for s in node.shapes.keys()}

            callee = TensorGraph(
                node.id, 'AssertShape', None, output, output, None, node.shapes)
            self.tensor_graph.append(callee)
        else:
            # test builtins
            call = node.calls[0]
            if call.name in _BuiltinsNode:
                callee = self._build_builtins(call.name, node)
                self.tensor_graph.append(callee)
                self.last_id = node.id
                return

            for call in node.calls:
                # Step 1. get the node
                callee = self.get(call.name)
                callee.id = node.id

                # Step 2. apply variables
                if call.args:
                    args = {k: self.graph.replace(v.value)
                            for k, v in call.args.items()}
                    callee.apply_variables(args, is_shortcut=True)

                # Step 3. apply IO
                inputs = call.inputs or {}
                for k in callee.get_input_shapes().keys():
                    if k not in inputs.keys():
                        inputs[k] = ast.Out(name=k)
                outputs = {k: ast.Out(node.id, k)
                           for k in callee.get_output_shapes().keys()}

                # set default IO to "x"
                inputs = inputs or {'x': ast.Out(name='x')}
                outputs = outputs or {'x': ast.Out(id=node.id, name='x')}

                callee.input = inputs
                callee.output = outputs

                # Step 4. merge shapes
                if self.tensor_graph:
                    last_outputs = {k: self._get_shape(x)
                                    for k, x in inputs.items()}
                    new_inputs = callee.get_input_shapes()

                    _merge_shapes(last_outputs, new_inputs)

                    # identity
                    new_outputs = callee.get_output_shapes()
                    for name in new_outputs.keys():
                        if not new_outputs[name]:
                            new_outputs[name] = new_inputs[name]
                elif inputs:
                    for x in inputs.values():
                        x.id = 0

                # Step 5. store
                self.tensor_graph.append(callee)

            # Step 6. merge dedicated shapes
            if node.shapes:
                outputs = self.get_output_shapes()
                _merge_shapes(node.shapes, outputs)

            # Step 7. store id
            self.last_id = node.id

    def get_output_shapes(self):
        for node in reversed(self.tensor_graph):
            outputs = node.get_output_shapes()
            if outputs:
                return outputs

    def _get_shape(self, out):
        for node in reversed(self.tensor_graph):
            # test id
            if out.id is not None:
                if node.id > out.id:
                    continue
                if node.id < out.id:
                    break

            shapes = node.get_output_shapes()
            if out.name in shapes.keys():
                out.id = node.id
                return shapes[out.name]
        raise Exception(f'no such input: {repr(out)}')

    def _update_out_id(self, out):
        if out.id is not None:
            return out
        for node in reversed(self.tensor_graph):
            shapes = node.get_output_shapes()
            if out.name in shapes.keys():
                out.id = node.id
                return out
        raise Exception(f'no such input: {repr(out)}')

    def get(self, name):
        if name in self.children.keys():
            return self.children[name].clone(self.root, [])
        return self.parent.get(name)

    def build(self):
        return NodeIR(self.name, self.graph, self.tensor_graph)

    def _build(self, file, parent=None):
        return self.parent._build(file, parent)

    def _build_builtins(self, name, node):
        if name == 'Transform':
            return self._build_transform(node)
        if name == 'Concat':
            return self._build_concat(node)
        raise NotImplementedError

    def _build_transform(self, node):
        call = _assert_tensor_graph_name(node, ['Transform'], sized=True)

        # Step 1. get the IO
        inputs = self.get_output_shapes()
        outputs = node.shapes

        # Step 2. match the tuple
        input_keys = inputs.keys()
        output_keys = outputs.keys()
        if input_keys != output_keys:
            input_keys = ', '.join(input_keys)
            output_keys = ', '.join(output_keys)
            raise Exception(
                f'Expected tuple ({input_keys}), Given ({output_keys})')

        # Step 3. match the size
        for name in input_keys:
            input = build_variable(inputs[name].product())
            output = build_variable(outputs[name].product())
            if ast.is_hint(input) or ast.is_hint(output):
                # TODO: FUTURE: implement comparing hinted values
                print('warning: comparing hinted values is not supported yet!')
            else:
                assert input == output, f'Expected product {input}, Given {output}'

        # Step 4. apply to tensor graph
        id = self.last_id + 1
        input = {s: self._update_out_id(ast.Out(name=s))
                 for s in inputs.keys()}
        output = {s: ast.Out(id, s)
                  for s in outputs.keys()}

        # Step 5. store
        kwargs = {'output_shapes': outputs}
        return TensorGraph(node.id, call.name, kwargs, input, output, inputs, outputs)

    def _build_concat(self, node):
        call = _assert_tensor_graph_name(
            node, ['Concat'], inputs=list, args=True)

        # Step 1. get the axis
        axis = call.get_arg('axis')
        axis = self.graph.replace(axis.value)
        axis = build_variable(axis)

        # Step 2. get the inputs
        inputs = [self._get_shape(x) for x in call.inputs]

        # Step 3. concat the inputs
        assert len(inputs) >= 1, 'unexpected empty shapes'
        assert isinstance(axis, int), f'unexpected axis typeL {axis.__name__}'
        tensor_base = copy(inputs[0].dims)
        tensor_dims = len(tensor_base)

        if axis < 0:
            axis = -axis - tensor_dims
        assert 0 <= axis and axis < tensor_dims, f'Expected (0 <= "{axis}" < {tensor_dims}): {call.name}'

        target_dim = ast.Shape([tensor_base[axis]])
        tensor_base[axis] = None

        for shape in inputs[1:]:
            assert len(
                shape) == tensor_dims, f'Expected <{tensor_dims}> dims Tensor, Given <{len(shape)}>{shape}'
            for d0, d1 in zip(tensor_base, shape.dims):
                if d0 is None:
                    target_dim.dims.append(d1)
                    continue
                d0 = build_variable(d0)
                d1 = build_variable(d1)
                if ast.is_hint(d0) or ast.is_hint(d1):
                    # TODO: FUTURE: implement comparing hinted values
                    print('warning: comparing hinted values is not supported yet!')
                assert d0 == d1, f'Expected {d0}, Given {d1}'

        # Step 4. get the IO
        inputs = {'x': inputs}
        outputs = {'x': ast.Shape([target_dim.add()])}

        # Step 5. apply to tensor graph
        id = self.last_id + 1
        input = {'x': call.inputs}
        output = {s: ast.Out(id, s) for s in outputs.keys()}

        # Step 6. store
        kwargs = {'axis': axis}
        return TensorGraph(node.id, call.name, kwargs, input, output, inputs, outputs)


class ExternNodeContainer:
    def __init__(self, name, data, optim):
        super().__init__()
        self.name = name
        self.data = data
        self.optim = optim
        self.graph = None

        self.input = None
        self.output = None

    def add_tensor_graph(self, node: ast.GraphNode):
        is_input = node.id == 0 and not self.data

        name = 'Input' if is_input else 'Output'
        call = _assert_tensor_graph_name(node, [name])

        if is_input:
            self.input = node.shapes
        else:
            self.output = node.shapes

    def build(self):
        # set default IO to "x"
        if not (self.data or self.optim):
            input = {s: ast.Out(0, s) for s in self.input.keys()} \
                if self.input else {'x': ast.Out(0, 'x')}
        else:
            input = {}

        if not self.optim:
            output = {s: ast.Out(1, s) for s in self.output.keys()} \
                if self.output else {'x': ast.Out(1, 'x')}
        else:
            output = {}

        tensor_graph = TensorGraph(
            0, self.name, self.graph._variables, input, output, self.input, self.output)
        return NodeIR(self.name, self.graph, [tensor_graph])


class ExecIR(EnvVars):
    def __init__(self, name):
        super().__init__()
        self._name = name
        self._graph = None

    def clone(self, root, variables):
        cloned = ExecIR(self._name)
        cloned._graph = self._graph.clone(root.generate_id(), variables)

        for k, v in self._dict().items():
            for name in [k, f'_{k}_type', f'_{k}_shortcut', f'_{k}_help']:
                if hasattr(self, name):
                    setattr(cloned, name, getattr(self, name))
        return cloned

    def set(self, key, value):
        setattr(self, key, value)

    def _set_node(self, root, key, value):
        # Step 1. build
        ir = root.get(value)
        node = ir.build(root)

        # Step 2. store
        setattr(self, key, node)

    def apply_graph(self, graph):
        self._graph = graph
        for var in graph.get_variables().values():
            name = var.name.replace(' ', '_')
            ty = var.ty.to_python_type()
            value = build_variable(var.value)

            setattr(self, name, value)
            setattr(self, f'_{name}_type', ty)
            if var.shortcut:
                setattr(self, f'_{name}_shortcut', var.shortcut)

    def build(self, root):
        # Step 1. assert each variable is not none
        self._assert_not_none(self._name)

        # Step 2. apply to environment variables
        with self._use_exec(root):
            # Step 3. build nodes
            for var in self._graph.get_variables().values():
                value = getattr(self, var.name.replace(' ', '_'))
                if var.ty.is_node():
                    ir = root.node_root.get(value)
                    var.value = node = ir.build(root.node_root)
                else:
                    var.value = build_variable(value)

        # Step 3. get variables
        kwargs = {k: v.value for k, v in self._graph.get_variables().items()}

        # Step 4. build to extern exec node
        node_cls = root.node_root.get_extern(self._name)
        return node_cls(env=root.env, **kwargs)

    def _use_exec(self, root):
        class ReadOnlyExec:
            def __init__(self, exec, env):
                self._exec = exec
                self._env = env

            def __getattr__(self, name):
                if name == 'env':
                    return self._env
                if not name.startswith('_'):
                    return getattr(self._exec, name)

                # default behaviour
                return self.__getattribute__(name)

        class UseExec:
            def __init__(self, exec, root):
                super().__init__()
                self.exec = exec
                self.root = root

            def __enter__(self):
                env = self.root.env
                self.root.node_root.exec = ReadOnlyExec(self.exec, env)

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.root.node_root.exec = None

        return UseExec(self, root)


class NodeRoot:
    def __init__(self):
        super().__init__()
        self.exec = None

        self._seed = 1

        self._source_paths = {}
        self._sources = {}
        self._irs = {}

        self._externs = std.get_externs()
        self._extern_nodes = {}

        self._parser = Parser()

        for name, path in std.get_sources().items():
            self.add_source_path(name, path)

    def generate_id(self):
        id = self._seed
        self._seed += 1
        return id

    def add_source(self, source):
        file = self._parser.parse(source)
        self._sources[file.node.name] = file

    def add_source_path(self, name, path):
        self._source_paths[name] = path

    def add_extern(self, name, path):
        self._externs[name] = path

    def get(self, name):
        if name in self._irs.keys():
            return self._irs[name].clone(self, [])

        if name in self._source_paths.keys():
            path = self._source_paths.pop(name)
            with open(path, encoding='utf-8') as f:
                self.add_source(f.read())

        if name in self._sources.keys():
            result = self._irs[name] = self._build(self._sources.pop(name))
            return result.clone(self, [])
        raise Exception(f'undefined node: {name}')

    def get_extern(self, name):
        if name in self._extern_nodes.keys():
            return self._extern_nodes[name]

        if name in self._externs.keys():
            path = self._externs.pop(name)

            loader = importlib.machinery.SourceFileLoader('n3.extern', path)
            spec = importlib.util.spec_from_loader(loader.name, loader)
            mod = importlib.util.module_from_spec(spec)
            loader.exec_module(mod)

            if not hasattr(mod, name):
                raise Exception(
                    f'node class not defined in python script: {name}, "{path}"')
            node_cls = self._extern_nodes[name] = getattr(mod, name)
            return node_cls
        raise Exception(f'undefined extern node: {name}')

    def _build(self, file: ast.File, parent: NodeContainer = None):
        node = file.node
        parent = parent or self

        if node.ty.is_extern():
            return self._build_extern(file)
        if node.ty == ast.NodeType.EXEC:
            return self._build_exec(file)

        container = NodeContainer(parent, node.name)

        # Step 1. import remote models
        for use in file.uses:
            container.add_use(use)

        # Step 2. make a graph
        container.graph = self._make_graph(node.variables)

        # Step 3. hint variables with tensor graph
        for id, n in node.graph.items():
            if n.shapes:
                for x, shapes in n.shapes.items():
                    shapes.dims = container.graph.hint(
                        ast.Out(id, x), shapes.dims)

        # Step 4. re-define nodes (with)
        for w in node.withs.values():
            container.add_with(w)

        # Step 5. build children nodes
        for child in node.children.values():
            container.add_child(child)

        # Step 6. make a tensor graph
        last_id = 0
        for id, n in node.graph.items():
            if id - last_id != 1 and not (last_id == 0 and id == 0):
                raise Exception(f'Expected id {last_id+1}, Given {id}')
            container.add_tensor_graph(n)
            last_id = id

        # Step 7. store
        return container.build()

    def _build_extern(self, file: ast.File):
        node = file.node
        data = node.ty == ast.NodeType.DATA
        optim = node.ty == ast.NodeType.OPTIM
        container = ExternNodeContainer(file.node.name, data, optim)

        assert not node.withs, f'unexpected "with" syntax: {node.name}'
        assert not node.children, f'unexpected "node" syntax: {node.name}'

        # Step 1. make a graph
        container.graph = self._make_graph(node.variables)

        # Step 2. hint variables with tensor graph
        for id, n in node.graph.items():
            if n.shapes:
                for x, shapes in n.shapes.items():
                    shapes.dims = container.graph.hint(
                        ast.Out(id, x), shapes.dims)

        # Step 3. make a tensor graph
        num_tensor_graph = len(node.graph)
        if data:
            assert num_tensor_graph == 1, f'Expected Output node, Given {num_tensor_graph}'
        elif optim:
            assert num_tensor_graph == 0, f'unexpected "Graph" syntax: {node.name}'
        else:
            assert num_tensor_graph == 2, f'Expected Input & Output node, Given {num_tensor_graph}'

        last_id = -1
        for id, n in node.graph.items():
            if id - last_id != 1:
                raise Exception(f'Expected id {last_id+1}, Given {id}')
            container.add_tensor_graph(n)
            last_id = id

        # Step 4. store
        return container.build()

    def _build_exec(self, file: ast.File):
        node = file.node
        ir = ExecIR(node.name)

        assert not node.withs, f'unexpected "with" syntax: {node.name}'
        assert not node.children, f'unexpected "node" syntax: {node.name}'
        assert not node.graph, f'unexpected "graph" syntax: {node.name}'

        # Step 1. make a graph
        ir.apply_graph(self._make_graph(file.node.variables))

        # Step 2. store
        return ir

    def _make_graph(self, variables):
        return make_graph(self.generate_id(), variables)
