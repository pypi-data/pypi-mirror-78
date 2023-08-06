import abc
import os

from inflection import underscore

from .extern import ExternNodeBase
from ...util.dirs import DATA_DIR


class DataNode(ExternNodeBase, metaclass=abc.ABCMeta):
    def __init__(self, exec, **kwargs):
        super().__init__(**kwargs)
        name = underscore(self.__class__.__name__).replace('_', '-')
        self._dataset_dir = os.path.join(exec.env.root, DATA_DIR, name)
        self._batch_size = exec.batch_size

    @property
    def dataset_dir(self):
        return self._dataset_dir

    @property
    def batch_size(self):
        return self._batch_size

    def forward(self):
        raise Exception('data node cannot be directly called')

    @abc.abstractmethod
    def get_train_dataset(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_valid_dataset(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_eval_dataset(self):
        raise NotImplementedError
