import inflection
from copy import copy

from ..ast import clone_value
from .variable import build


class TensorGraph:
    def __init__(self, id, name, kwargs, input, output, input_shapes, output_shapes):
        super().__init__()
        self.id = id
        self.name = name
        self.kwargs = kwargs or {}
        self.input = input or {}
        self.output = output or {}

        self.input_shapes = input_shapes or {
            k: None for k in self.input.keys()}
        self.output_shapes = output_shapes or {
            k: None for k in self.output.keys()}

    def clone(self, root, variables):
        kwargs = clone_value(self.kwargs, variables)
        input_shapes = clone_value(self.input_shapes, variables)
        output_shapes = clone_value(self.output_shapes, variables)

        return TensorGraph(self.id, self.name, kwargs, copy(self.input), copy(self.output),
                           input_shapes, output_shapes)

    def get_input_shapes(self):
        return self.input_shapes

    def get_output_shapes(self):
        return self.output_shapes

    def build(self, root):
        kwargs = {inflection.underscore(k.title().replace(' ', '_')): build(v)
                  for k, v in self.kwargs.items()}

        node_cls = root.get_extern(self.name)
        return node_cls(exec=root.exec, input=self.input, output=self.output, **kwargs)

    def __repr__(self):
        kwargs = '\n\t[args]\n' + \
            '\n'.join(f'\t\t{repr(v)}' for v in self.kwargs.values())
        input = '\n\t[input]\n' + \
            '\n'.join(f'\t\t{k}: {repr(v)}{self.input_shapes[k]}'
                      for k, v in self.input.items())
        output = '\n\t[output]\n' + \
            '\n'.join(f'\t\t{k}: {repr(v)}{self.output_shapes[k]}'
                      for k, v in self.output.items())
        return self.name + kwargs + input + output
