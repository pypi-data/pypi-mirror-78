import glob
import os
import sys

import inflection
import tensorboardX
from tqdm import tqdm

from ..util.dirs import LOGS_DIR


class EpochIter:
    def __init__(self, dataset, bar):
        self._dataset = enumerate(dataset)
        self._bar = bar

    def __iter__(self):
        return self

    def __next__(self):
        idx, value = next(self._dataset)
        self._bar.update()
        return value


class Epoch:
    def __init__(self, writer, head, bar, num_batch, value):
        super().__init__()
        self._writer = writer
        self._head = head
        self._bar = bar
        self._num_batch = num_batch
        self._value = value

    def write(self, name, value, use_batch=False):
        if isinstance(value, (int, float)):
            if use_batch:
                value = value / self._num_batch
            self._write_scalar(name, value)
        else:
            raise Exception(f'not supported type: {type(value)}')

    def _write_scalar(self, name, value):
        self._writer.add_scalar(self._tag(name), value, self._value)

    def flush(self):
        return self._writer.flush()

    def _tag(self, name):
        return f'{self._head}/{name}'

    def __int__(self):
        return self._value

    def __repr__(self):
        return str(int(self))


class EpochWriter:
    def __init__(self, writer, head, fn_dataset, start, end):
        super().__init__()
        self._writer = writer
        self._head = head
        self._fn_dataset = fn_dataset
        self._start = start
        self._end = end

        self._bar = None

    def __iter__(self):
        return self

    def __next__(self):
        if self._start == self._end:
            self._bar.close()
            raise StopIteration

        dataset = self._fn_dataset()

        if self._bar is None:
            self._num_batch = len(dataset)
            self._bar = tqdm(total=(self._end - self._start) * self._num_batch)

        epoch = Epoch(self._writer, self._head, self._bar,
                      self._num_batch, self._start)
        self._start += 1

        return epoch, EpochIter(iter(dataset), self._bar)


class ExecWriter:
    def __init__(self, env, exec):
        super().__init__()
        self._exec_name = inflection.underscore(exec.get_name())
        self._model_name = inflection.underscore(exec.model.get_name())

        logdir = os.path.join(env.root, LOGS_DIR,
                              self._exec_name, self._model_name)
        logdir = _increment_dir(logdir)

        self._writer = tensorboardX.SummaryWriter(logdir)
        self._epoch = exec.epoch

    def do_epoch(self, tag, fn_dataset):
        tag = f'{self._exec_name}/{tag}'
        return EpochWriter(self._writer, tag, fn_dataset, 0, self._epoch)


def spawn_daemon(env):
    from tensorboard.main import run_main

    logdir = os.path.join(env.root, LOGS_DIR)
    sys.argv = [sys.argv[0]] + ['--logdir', logdir] + sys.argv[3:]
    run_main()


def _increment_dir(logdir):
    num_dirs = len(glob.glob(rf'{logdir}/exp*/'))
    return os.path.join(logdir, f'exp{num_dirs}')
