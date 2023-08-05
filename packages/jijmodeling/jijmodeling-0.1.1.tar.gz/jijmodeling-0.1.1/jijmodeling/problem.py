from jijmodeling.array.array import Array
from jijmodeling.express import Constraint
from typing import TypeVar, Generic

Var = TypeVar('T')

class Problem(Generic[Var]):
    def __init__(self, problem_name: str) -> None:
        self.variables = []
        self.name = problem_name
        self.model = 0
        self.cost = 0
        self.constraints = {}

    def var(self, variable: Var)->Var:
        # if not isinstance(variable, Variable):
        #     raise TypeError('variable should be jijmodeling.Variable')
        self.variables.append(variable)
        return variable

    
    def __repr__(self) -> str:
        return '{}: {}'.format(self.name, self.model)


    def __add__(self, other):
        if self.model == 0:
            self.model = other
        else:
            self.model += other

        if isinstance(other, Constraint):
            self.constraints[other.label] = other
        else:
            self.cost = other if self.cost == 0 else self.cost + other

        return self


    def to_pyqubo(self, index: dict={}, placeholder: dict={}, fixed_variables: dict={}):
        self._placeholder = placeholder
        self._fixed_variables = fixed_variables
        return self.model.to_pyqubo(index=index, placeholder=placeholder, fixed_variables=fixed_variables)

 
    def decode_dimod_resopnse(self, response):
        decoded = []
        for i in range(len(response)):
            res = response.slice(i, i+1)
            vars_value = {}
            for var in self.variables:
                vars_value.update(var.decode_dimod_response(res, self._placeholder))
            
            # replace fixed variables
            for label, fixed_val in self._fixed_variables.items():
                label_list = label.split('[')
                val_label = label_list[0]
                index = [int(i[:-1]) for i in label_list[1:]]
                vars_value[val_label][tuple(index)] = fixed_val
            decoded.append(vars_value)

        return decoded

    def calc_penalty(self, solution):
        penalties = {}
        for k, const in self.constraints.items():
            penalties[k] = const.value(solution, self._placeholder)
            if const.condition == '==' and penalties[k] == const.constant:
                penalties[k] = 0.0
            elif const.condition == '<=' and penalties[k] <= const.constant:
                penalties[k] = 0.0
            else:
                penalties[k] = const.value(solution, self._placeholder) - const.constant
        return penalties

    def calc_cost(self, solution):
        return self.cost.value(solution, self._placeholder)


    def from_serializable(self, serializable: dict):
        import jijmodeling
        className = serializable['class'].split('.')[1:]
        cls = getattr(jijmodeling, className)
        return cls.from_serializable(serializable)