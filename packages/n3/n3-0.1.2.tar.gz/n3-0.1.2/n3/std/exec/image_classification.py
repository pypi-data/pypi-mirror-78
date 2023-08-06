from n3.builder import *


class ImageClassification(Trainer):
    def eval(self):
        raise NotImplementedError
