from abc import ABCMeta

class Variable(metaclass=ABCMeta):
    def __init__(self, label: str):
        self._label = label
        self.var_label = label

    @property
    def label(self):
        return self._label

    def set_relabel(self, label: str):
        self._label = label
