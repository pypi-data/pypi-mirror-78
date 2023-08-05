from jijmodeling.variables import placeholder
from jijmodeling.variables.variable import Variable
from jijmodeling.variables.to_pyqubo import ToPyQUBO
from jijmodeling.express.express import Express
import pyqubo


class DisNum(Express, Variable, ToPyQUBO):
    def __init__(self, label: str, lower: float=0.0, upper: float=1.0, bits: int=3):
        super().__init__([])
        self._label = label
        self.lower = lower
        self.upper = upper
        self.bits = bits

    def __repr__(self) -> str:
        return self.label

    def to_pyqubo(self, index:dict={}, placeholder:dict={}, fixed_variables: dict = {}):
        if self.label in fixed_variables:
            return fixed_variables[self.label]
        var_label = self.label + '[{}]'
        coeff = (self.upper - self.lower)/(2**self.bits - 1)
        return coeff * sum(2**i * pyqubo.Binary(var_label.format(i)) for i in range(self.bits)) + self.lower