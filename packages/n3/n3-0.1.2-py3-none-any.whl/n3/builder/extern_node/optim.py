import abc

import torch.optim as optim

from .extern import ExternNodeBase


class OptimNode(ExternNodeBase, metaclass=abc.ABCMeta):
    _inner: optim.Optimizer = None

    def forward(self):
        raise Exception('optim node cannot be directly called')

    @abc.abstractmethod
    def _initialize(self, models):
        pass

    def initialize(self, *models):
        if self._inner is None:
            params = [p for m in models for p in m.parameters()]
            self._inner = self._initialize(params)

    def zero_grad(self):
        self._inner.zero_grad()

    def step(self):
        self._inner.step()
