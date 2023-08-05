import pyqubo

from jijmodeling.variables.to_pyqubo import ToPyQUBO
from jijmodeling.express.express import Express, from_serializable

class Constraint(Express, ToPyQUBO):
    def __init__(self, label: str, term, condition='==', constant=0, with_mul=True):
        super().__init__([term])
        self.label = label
        self.condition = condition
        self.constant = constant
        self.with_mul = with_mul

    def to_pyqubo(self, **kwargs) -> pyqubo.Express:
        term = self.children[0].to_pyqubo(**kwargs)
        if self.with_mul:
            return pyqubo.Placeholder(self.label) * pyqubo.Constraint(term, self.label)
        return pyqubo.Constraint(term, self.label)

    def value(self, solution, placeholder):
        return self.children[0].value(solution, placeholder)

    @classmethod
    def from_serializable(cls, seriablizable: dict):
        term = from_serializable(seriablizable['attributes']['children'])[0]
        label = from_serializable(seriablizable['attributes']['label'])
        condition = from_serializable(seriablizable['attributes']['condition'])
        constant = from_serializable(seriablizable['attributes']['constant'])
        with_mul = from_serializable(seriablizable['attributes']['with_mul'])
        return cls(label, term, condition, constant, with_mul)