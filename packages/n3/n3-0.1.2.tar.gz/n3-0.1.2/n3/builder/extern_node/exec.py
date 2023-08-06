import abc
import os

import torch
import inflection

from .data import DataNode
from .node import Node
from .optim import OptimNode
from ...writer import ExecWriter


class ExecNode(metaclass=abc.ABCMeta):
    def __init__(self, env, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self._writer = ExecWriter(env, self)

    def get_name(self):
        return self.__class__.__name__


class Trainer(ExecNode, metaclass=abc.ABCMeta):
    data: DataNode
    model: Node  # TODO: dynamically init, for applying dimensions of data

    loss: Node
    optimizer: OptimNode

    epoch: int
    batch_size: int

    def __init__(self, env, **kwargs):
        super().__init__(env, **kwargs)
        self.train_dataset = None

    def train(self):
        # Step 1. ready to train
        self._train_begin()

        # Step 2-1. peek the IO
        for epoch, dataset in self._writer.do_epoch('train', self.data.get_train_dataset):
            self._train_epoch_begin(epoch)

            loss_sum = 0.0

            for idx, data in enumerate(dataset):
                x, y = self._train_iter_begin(data)
                # Step 2-2. clean-up gradients
                self.optimizer.zero_grad()
                # Step 2-3. predict classses
                y_pred = self.model(**x)
                # Step 2-4. calculate difference (loss)
                loss = self.loss(**y_pred, **y)['x']
                # Step 2-5. calculate gradients
                loss.backward()
                # Step 2-6. step
                self.optimizer.step()
                # Step 2-7. store result
                loss_sum += loss.item()

            # Step 2-8. store log
            self._train_epoch_end(epoch, loss=loss_sum)

        # Step 3. clean up
        self._train_end()

    def _train_begin(self):
        self.optimizer.initialize(self.model)

    def _train_epoch_begin(self, epoch):
        self.model.train()

    def _train_iter_begin(self, data):
        return {'x': data[0]}, {'y': data[1]}

    def _train_epoch_end(self, epoch, **metrics):
        for name, value in metrics.items():
            epoch.write(name, value, use_batch=True)
        epoch.flush()

    def _train_end(self):
        pass

    @abc.abstractmethod
    def eval(self):
        raise NotImplementedError

    def publish(self, args):
        # Step 1. ready to publish
        self.model.eval()

        # Step 2. get dummy input
        x, _ = next(iter(self.data.get_train_dataset()))

        # Step 3. get parameters
        input_names = ['x']  # 모델의 입력값을 가리키는 이름
        output_names = ['out_x']  # 모델의 출력값을 가리키는 이름
        dynamic_axes = {'x': {0: 'batch_size'},  # 가변적인 길이를 가진 차원
                        'out_x': {0: 'batch_size'}}

        export_params = True  # 모델 파일 안에 학습된 모델 가중치를 저장할지의 여부
        opset_version = 10  # 모델을 변환할 때 사용할 ONNX 버전
        do_constant_folding = True  # 최적하시 상수폴딩을 사용할지의 여부

        name = inflection.underscore(self.model.get_name())
        output_path = os.path.join(args.output_path, f'{name}.onnx')

        # Step 4. export to onnx
        torch.onnx.export(self.model, {'x': x}, output_path,
                          input_names=input_names,
                          output_names=output_names,
                          dynamic_axes=dynamic_axes,

                          export_params=export_params,
                          opset_version=opset_version,
                          do_constant_folding=do_constant_folding,
                          )

        # Step 5. do target-specific publishing
        # TODO: to be implemented
