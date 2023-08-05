from typing import Dict, Type

from numpy.lib.function_base import place

from jijmodeling.variables.to_pyqubo import ToPyQUBO
from jijmodeling.express.express import Express
from jijmodeling.variables.variable import Variable
import pyqubo
import numpy as np


class Placeholder(Express, Variable, ToPyQUBO):
    """This class represents placeholder for lazy evaluation.

    Args:
        Express ([type]): [description]
        Variable ([type]): [description]
        ToPyQUBO ([type]): [description]
    """
    def __init__(self, label: str):
        self._label = label
        super().__init__([])

    def __repr__(self):
        return self._label

    @property
    def label(self):
        return self._label

    @classmethod
    def from_serializable(cls, seriablizable: dict):
        label = seriablizable['attributes']['_label']
        return cls(label=label)

    def to_pyqubo(self, index: Dict[str, int]={}, placeholder: dict={}, fixed_variables: dict={}) -> pyqubo.Express:

        if self.label in placeholder:
            # placeholder value is not Express
            if isinstance(placeholder[self.label], Express):
                raise TypeError("placeholder's value is not Express class.")
            return placeholder[self.label]


        label_list = self.label.split('[')
        label = label_list[0]
        indices = [int(l[:-1]) for l in label_list[1:]]
        if label in placeholder:
            if isinstance(placeholder[label], np.ndarray):
                return placeholder[label][tuple(indices)]
            else:
                return placeholder[label]
        else:
            return pyqubo.Placeholder(label=self.label)
