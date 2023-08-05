from typing import List, Any, Union, Dict
from abc import ABCMeta

import pyqubo
from jijmodeling.variables.to_pyqubo import ToPyQUBO, to_pyqubo


class Express(metaclass=ABCMeta):
    """All component inheritance this class.
    This class provide computation rules.
    """
    def __init__(self, children: List[Any]):
        self.children = children
        index_labels = []
        for child in self.children:
            if isinstance(child, Express):
                index_labels += child.index_labels
        self.index_labels = list(set(index_labels))

    def __sub__(self, other):
        return self.__add__(-1*other)

    def __rsub__(self, other):
        return Add(other, -1*self)

    def __lsub(self, other):
        return self.__add__(-1*other)
    
    def __add__(self, other):
        return Add(self, other)

    def __radd__(self, other):
        return self.__add__(other)

    def __ladd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        return Mul(self, other)
    
    def __lmul__(self, other):
        return self.__mul__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, other):
        return Power(self, other)

    def __repr__(self):
        str_repr = ""
        for child in self.children:
            str_repr +=  child.__repr__() + " "
        return str_repr[:-1]

    def to_serializable(self):
        def express_to_ser(s):
            if 'to_serializable' in dir(s):
                return s.to_serializable()
            elif isinstance(s, (list, tuple)):
                return {
                    'iteratable': 'list' if isinstance(s, list) else 'tuple',
                    'value': [express_to_ser(t) for t in s],
                }
            elif isinstance(s, dict):
                return {k: express_to_ser(v) for k,v in s.items()}
            else:
                return s
        serializable = {
            'class': self.__class__.__module__ + '.' + self.__class__.__name__,
            'attributes': {k: express_to_ser(v) for k, v in vars(self).items()}
        }
        return serializable

    @classmethod
    def from_serializable(cls, seriablizable: dict):
        _cls_serializable_validation(seriablizable, cls)
        children = from_serializable(seriablizable['attributes']['children'])
        return cls(children)


TermType = Union[Express, int, float]
        

class Add(Express, ToPyQUBO):
    def __init__(self, *terms: TermType):
        super().__init__(list(terms))

    def __add__(self, other):
        self.children.append(other)
        return self

    def __repr__(self):
        str_repr = ""
        for t in self.children:
            str_repr += t.__repr__() + ' + '
        return str_repr[:-3]


    def to_pyqubo(self, index: Dict[str, int]={}, placeholder: dict={}, fixed_variables: dict={}) -> pyqubo.Express:

        return sum(to_pyqubo(child, index=index, placeholder=placeholder, fixed_variables=fixed_variables) for child in self.children)

    def value(self, solution, placeholder={}, index={}):
        def to_value(term):
            if isinstance(term, Express):
                return term.value(solution, placeholder, index)
            else:
                return term
        return sum(to_value(child) for child in self.children)

    @classmethod
    def from_serializable(cls, seriablizable: dict):
        children = from_serializable(seriablizable['attributes']['children'])
        return cls(*children)

class Mul(Express, ToPyQUBO):
    def __init__(self, *terms: TermType):
        super().__init__(list(terms))

    def __mul__(self, other):
        self.children.append(other)
        return self

    def __repr__(self):
        str_repr = ""
        for t in self.children:
            if isinstance(t, Add) and len(t.children) > 1:
                str_repr += '(%s)' % t.__repr__()
            if isinstance(t, (int, float)):
                str_repr += '({})'.format(t.__repr__())
            else:
                str_repr += t.__repr__()
        return str_repr

    def to_pyqubo(self, **kwargs) -> pyqubo.Express:
        term = 1
        for child in self.children:
            term *= child.to_pyqubo(**kwargs) if isinstance(child, ToPyQUBO) else child
        return term

    def value(self, solution, placeholder, index):
        term = 1
        def to_value(term):
            if isinstance(term, Express):
                return term.value(solution, placeholder, index)
            else:
                return term

        for child in self.children:
            term *= to_value(child)
        return term 

    @classmethod
    def from_serializable(cls, seriablizable: dict):
        children = from_serializable(seriablizable['attributes']['children'])
        return cls(*children)

class Power(Express, ToPyQUBO):
    def __init__(self, base: TermType, exponent: int):
        super().__init__([base, exponent])
        self.base = base
        self.exponent = exponent

    def to_pyqubo(self, **kwargs) -> pyqubo.Express:

        term = to_pyqubo(self.base, **kwargs)

        return term ** self.exponent


    def __repr__(self) -> str:
        return '({})^{}'.format(self.base, self.exponent)


    def value(self, solution, placeholder={}, index={}):
        value = self.base.value(solution, placeholder, index)
        return value ** self.exponent

    @classmethod
    def from_serializable(cls, seriablizable: dict):

        base = from_serializable(seriablizable['attributes']['base'])
        exponent = from_serializable(seriablizable['attributes']['exponent'])
        return cls(base, exponent)



def from_serializable(serializable):

    if isinstance(serializable, dict) and 'class' in serializable:
        import jijmodeling
        modulePath = serializable['class'].split('.')[2:]
        module = jijmodeling
        for m in modulePath:
            module = getattr(module, m)
        _cls_serializable_validation(serializable, module)
        return module.from_serializable(serializable)

    elif isinstance(serializable, dict) and 'iteratable' in serializable:
        if serializable['iteratable'] == 'list':
            return [from_serializable(s) for s in serializable['value']]
        elif serializable['iteratable'] == 'tuple':
            return tuple(from_serializable(s) for s in serializable['value'])
    elif isinstance(serializable, list):
        return [from_serializable(s) for s in serializable]
    elif isinstance(serializable, dict):
        return {k: from_serializable(v) for k, v in serializable.items()}
    else:
        return serializable

def _cls_serializable_validation(serializable, cls):
    if 'class' not in serializable:
        return
    class_name = serializable['class'].split('.')[-1]
    if cls.__name__ != class_name:
        raise ValueError('Class "{}" is not class "{}".'.format(cls.__name__, class_name))