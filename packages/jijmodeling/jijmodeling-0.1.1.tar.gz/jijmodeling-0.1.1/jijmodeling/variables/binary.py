from typing import Dict
from jijmodeling.variables.to_pyqubo import ToPyQUBO
from jijmodeling.express.express import Express
from jijmodeling.variables.variable import Variable
import pyqubo
import numpy as np


class Binary(Express, Variable, ToPyQUBO):

    def __init__(self, label: str) -> None:
        super().__init__([])
        self._label = label
        self.var_label = label

    def __repr__(self) -> str:
        return self.label

    def to_pyqubo(self, index: Dict[str, int]={}, placeholder: dict={}, fixed_variables: dict={}):
        """Convert to pyqubo.Binary class

        Returns:
            pyqubo.Binary: pyqubo object
        """

        if self.label in fixed_variables:
            return fixed_variables[self.label]

        return pyqubo.Binary(self.label)

    def decode_dimod_response(self, response, shape=None) -> dict:
        var_value_dict = {}
        dim = len(shape)

        if shape is None:
            for sample in response.samples():
                var_value_dict[self.var_label] = sample[self.label]
        else:
            for sample in response.samples():
                value_tensor = np.full(shape, np.nan, dtype=np.int)
                for key, value in sample.items():
                    label_list = key.split('[')
                    res_label = label_list[0]
                    if res_label == self.var_label:
                        indices = [int(k[:-1]) for k in label_list[-1*dim:]]
                        value_tensor[tuple(indices)] = value
                var_value_dict[self.var_label] = value_tensor

        return var_value_dict

            