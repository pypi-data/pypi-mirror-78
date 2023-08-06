import abc

import torch.nn as nn

from ... import ast


def _index(data, key):
    # indices
    if isinstance(key, list):
        return [_index(data, k) for k in key]
    return data[key]


class Node(nn.Module, metaclass=abc.ABCMeta):
    def get_name(self):
        return self.__class__.__name__

    def __repr__(self, depth=0):
        return super().__repr__()


class NodeExecutable(Node):
    def __init__(self, name, input, output, tensor_graph):
        super().__init__()
        self._name = name
        self._node_input = input
        self._node_output = output
        self._tensor_graph = nn.ModuleList(tensor_graph)

    def get_name(self):
        return self._name

    def __call__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], dict) and not kwargs:
            return self(**args[0])

        output = {ast.Out(0, k): x for k, x in kwargs.items()}

        for node in self._tensor_graph:
            x = {k: _index(output, n) for k, n in node._node_input.items()}
            x = node(**x)
            if not isinstance(x, dict):
                x = {'x': x}
            x = {n: x[k] for k, n in node._node_output.items()}
            output = {**output, **x}

        return {k.name: v for k, v in x.items()}

    def __repr__(self, depth=0):
        indent = ' ' * (depth * 4) + ' ' * 2
        indent_node = ' ' * ((depth+1) * 4)

        prefix = '' if depth else '* '

        name = f'{prefix}[node object {self._name}]'
        input = f'\n{indent}[input]\n' + \
            '\n'.join(f'{indent_node}{k}: {repr(v)}'
                      for k, v in self._node_input.items())
        output = f'\n{indent}[output]\n' + \
            '\n'.join(f'{indent_node}{k}: {repr(v)}'
                      for k, v in self._node_output.items())
        tensor_graph = '\n'.join(f'{indent}({id}) {n.__repr__(depth+1)}'
                                 for id, n in enumerate(self._tensor_graph))
        return name + input + output + '\n' + tensor_graph
