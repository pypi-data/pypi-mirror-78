from abc import *


class Use(metaclass=ABCMeta):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __repr__(self):
        return f'use {self.name}'


class UseByLocal(Use):
    def __init__(self, name, *_):
        super().__init__(name)


class UseByAuthor(Use):
    def __init__(self, name, author):
        super().__init__(name)
        self.author = author

    def __repr__(self):
        return f'{super().__repr__()} by {self.author}'


class UseByWeb(Use):
    def __init__(self, name, url):
        super().__init__(name)
        self.url = url

    def __repr__(self):
        return f'{super().__repr__()} by w{self.url}'
