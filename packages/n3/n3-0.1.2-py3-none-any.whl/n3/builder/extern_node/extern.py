import abc

from .node import Node


_MAGIC_VARIABLES = ['exec']


class ExternNodeBase(metaclass=abc.ABCMeta):
    def __init__(self, input, output, **kwargs):
        super().__init__()
        self._node_input = input
        self._node_output = output

        for k, v in kwargs.items():
            if k in _MAGIC_VARIABLES:
                continue
            setattr(self, k, v)

    @abc.abstractmethod
    def forward(self, **kwargs):
        raise NotImplementedError

    def __repr__(self, depth=0):
        indent = ' ' * (depth * 4) + ' ' * 2
        indent_node = ' ' * ((depth+1) * 4)

        name = f'[node extern object {self.__class__.__name__}]'
        input = f'\n{indent}[input]\n' + \
            '\n'.join(f'{indent_node}{k}: {repr(v)}'
                      for k, v in self._node_input.items())
        output = f'\n{indent}[output]\n' + \
            '\n'.join(f'{indent_node}{k}: {repr(v)}'
                      for k, v in self._node_output.items())
        return name + input + output


class ExternNode(Node, ExternNodeBase, metaclass=abc.ABCMeta):
    def __init__(self, input, output, **kwargs):
        Node.__init__(self)
        ExternNodeBase.__init__(self, input, output, **kwargs)
        self._node_input = input
        self._node_output = output

        for k, v in kwargs.items():
            setattr(self, k, v)

    @abc.abstractmethod
    def forward(self, **kwargs):
        raise NotImplementedError
