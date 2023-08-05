from typing import List, Tuple, Union, Type, Dict
import numbers

from numpy.lib.function_base import place
from pyqubo import array

from jijmodeling.variables.variable import Variable
from jijmodeling.variables.to_pyqubo import ToPyQUBO, to_pyqubo
from jijmodeling.variables.binary import Binary
from jijmodeling.variables.placeholder import Placeholder
from jijmodeling.sum import Sum
from jijmodeling.express.express import Express, from_serializable
import pyqubo
import numpy as np


class Tensor(Express, ToPyQUBO):
    """Tensor class for each variables

    Args:
        label
    """

    def __init__(self, label: str, variable, shape: tuple, indices: List[str]):
        """Tensor class for each variables

        Args:
            label (str): label for variable
            variable ([type]): variable object
            shape (tuple): shape of variable tensor
            indices (List[str]): index labels
        """
        super().__init__([])
        self.label = label
        self.variable = variable
        self.index_labels = indices
        self.shape = (shape, ) if isinstance(shape, int) else shape

    def __repr__(self):
        index_str = ''
        for i in self.index_labels:
            index_str += '[%s]' % i
        return self.label + index_str

    def to_pyqubo(self, index: Dict[str, int]={}, placeholder: dict={}, fixed_variables: dict={}) -> Union[pyqubo.Express, numbers.Number]:
        index_label = self.label

        for label in self.index_labels:
            if not isinstance(label, str):
                _label = to_pyqubo(label, index=index, placeholder=placeholder, fixed_variables=fixed_variables)
                index_label += '[%d]' % _label
            else:
                index_label += '[%d]' % index[label]
        
        if index_label in fixed_variables:
            return fixed_variables[index_label]

        self.variable.set_relabel(index_label)
        return self.variable.to_pyqubo(index=index, placeholder=placeholder, fixed_variables=fixed_variables)

    def value(self, solution, placeholder, index):
        if self.label in solution:
            sol = solution[self.label]
        elif self.label in placeholder:
            sol = placeholder[self.label]

        def to_index(obj):
            if isinstance(obj, str):
                return index[obj]
            else:
                return to_pyqubo(obj, placeholder=placeholder)
        index_label = [to_index(label) for label in self.index_labels]
        return sol[tuple(index_label)]

    @classmethod
    def from_serializable(cls, seriablizable: dict):
        label = from_serializable(seriablizable['attributes']['label'])
        variable = from_serializable(seriablizable['attributes']['variable'])
        shape = from_serializable(seriablizable['attributes']['shape'])
        indices = from_serializable(seriablizable['attributes']['index_labels'])
        return cls(label, variable, tuple(shape), indices)






class ArraySizePlaceholder(Placeholder):

    def __init__(self, label:str) -> None:
        super().__init__(label)
        self._array = None

    @property
    def array(self):
        return self._array

    def set_array(self, array, shape_index: int):
        self._array = array
        self._shape_index = shape_index
    
    def to_pyqubo(self, index: Dict[str, int]={}, placeholder: dict={}, fixed_variables: dict={}) -> pyqubo.Express:
        array_data = placeholder[self._array.label]
        if isinstance(array_data, Express):
            raise TypeError('Placeholder "{}" should not be Express class.'.format(self._array.label))

        if isinstance(array_data.shape[self._shape_index], Express):
            raise TypeError('Placeholder "{}" should not be Express class.'.format(self._array.label))
        return array_data.shape[self._shape_index]

    def __eq__(self, other):
        if not isinstance(other, ArraySizePlaceholder):
            return False
        return self.label == self.label

    def __hash__(self):
        return hash(self.label)

    def to_serializable(self):

        return {
            'class': self.__class__.__module__ + '.' + self.__class__.__name__,
            'attributes': {
                'children': [],
                'label': self.label,
                '_array': self._array.to_serializable(),
                '_shape_index': self._shape_index
            },
        }

    @classmethod
    def from_serializable(cls, seriablizable: dict):
        placeholder = cls(seriablizable['attributes']['label'])
        placeholder.set_array(
            array=Array.from_serializable(seriablizable['attributes']['_array']),
            shape_index=seriablizable['attributes']['_shape_index']
        )
        return placeholder




class Array(Variable):
    """Tensor object generator
    This class generate Tensor class by index access

    """
    def __init__(self, variable, shape: Union[int, tuple, ArraySizePlaceholder, None]):
        self.variable = variable
        self._label = variable.label
        shape_list = list(shape) if isinstance(shape, tuple) else [shape] 
        for i, s in enumerate(shape_list):
            if isinstance(s, ArraySizePlaceholder):
                if s.array is None:
                    s.set_array(self, i)
                shape_list[i] = s
        self._shape = shape_list

        self.dim = len(self._shape)

    def to_serializable(self):
        def express_to_ser(s):
            if 'to_serializable' in dir(s):
                return s.to_serializable()
            elif isinstance(s, list):
                return [express_to_ser(t) for t in s]
            else:
                return s
        
        # shape が　ArraySizePlaceholder の場合,
        # このクラスへの参照を持つのでそれは避けるようにする
        variables = vars(self)
        variables['shape'] = self._shape


        serializable = {
            'class': self.__class__.__module__ + '.' + self.__class__.__name__,
            'attributes': {k: express_to_ser(v) for k, v in variables.items()}
        }

        return serializable

    @classmethod
    def from_serializable(cls, serializable):
        variable = from_serializable(serializable['attributes']['variable'])
        shape = from_serializable(serializable['attributes']['shape'])
        return cls(variable, shape)
    
    @property
    def shape(self):
        shape = []
        for i, s in enumerate(self._shape):
            if s is None:
                asph = ArraySizePlaceholder(label=self.label + '_shape_%d' % i)
                asph.set_array(self, i)
                shape.append(asph)
            else:
                shape.append(s)
        return tuple(shape)


    def __getitem__(self, key: Union[str, slice, Tuple[Union[str, slice], ...]])->Type[Express]:
        """Gerate Tensor class

        Args:
            key (Union[str, slice, Tuple[Union[str, slice], ...]]): [description]

        Raises:
            ValueError: [description]

        Returns:
            Type[Express]: [description]
        """
        if not isinstance(key, tuple):
            key = (key, )

        if len(key) != self.dim:
            raise ValueError("{}'s dimension is {}.".format(self.label, self.dim))

        indices: List[str] = []
        summation_index = []
        for i, k in enumerate(list(key)):
            # for syntaxsugar x[:]
            if isinstance(k, slice):
                indices.append(':_{}'.format(i))
                summation_index.append((i, indices[i]))
            elif isinstance(k, (int, str, Express)):
                indices.append(k)

        term = Tensor(self.label, self.variable, self.shape, indices)

        # for syntaxsugar x[:]
        for i, ind in summation_index:
            term = Sum({ind: self.shape[i]}, term)

        return term

    def decode_dimod_response(self, response, placeholder)->dict:
        # decode shape
        _shape = tuple([to_pyqubo(s, placeholder=placeholder) for s in self.shape])
        return self.variable.decode_dimod_response(response, shape=_shape)