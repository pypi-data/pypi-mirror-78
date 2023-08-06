from abc import ABCMeta

class Variable(metaclass=ABCMeta):
    def __init__(self, label: str):
        self.label = label