from typing import List, Union, Tuple, Type

import numpy as np
import pyqubo

from jijmodeling.express.express import Express
from jijmodeling.express.express import from_serializable
from jijmodeling.variables.to_pyqubo import ToPyQUBO, to_pyqubo

class Sum(Express, ToPyQUBO):
    def __init__(self, indices: dict, term: Union['Sum', Type[Express]]):
        super().__init__(children=[term])
        self.indices = indices

        index_keys = list(indices.keys())
        self.index_labels = [ind for ind in self.index_labels if ind not in index_keys]

    def to_pyqubo(self, index: dict={}, placeholder: dict={}, fixed_variables: dict ={})->Union[int, float, pyqubo.Express]:
        term = self.children[0]
        sum_index = _reshape_to_index_set(self.indices, index, placeholder)
        return sum(term.to_pyqubo(index=ind, placeholder=placeholder, fixed_variables=fixed_variables) for ind in sum_index)

    def __repr__(self):
        repr_str = 'Σ_{'
        for i in self.indices.keys():
            repr_str += i + ', '
        term = self.children[0]
        repr_str = repr_str[:-2] + '}}({})'.format(term.__repr__()) 
        return repr_str

    def value(self, solution, placeholder={}, index={}):
        sum_index = _reshape_to_index_set(self.indices, index, placeholder)
        term = 0
        for child in self.children:
            for ind in sum_index:
                if isinstance(child, Express):
                    child_val = child.value(solution, placeholder, ind)
                    term += child_val if child_val is not None else 0
                else:
                    term += child
        return term

    @classmethod
    def from_serializable(cls, seriablizable: dict):
        indices = from_serializable(seriablizable['attributes']['indices'])
        term = from_serializable(seriablizable['attributes']['children'])[0]
        return cls(indices, term)
        




def _reshape_to_index_set(indices: dict, assigned_ind: dict, placeholder)->List[dict]:
    from jijmodeling.array import ArraySizePlaceholder
    index_lists = {}
    for label, V in indices.items():
        # TODO: corresponds to list of ArraySizePlaceholder
        if isinstance(V, (list, np.ndarray)):
            index, index_set = _satisfied_index_set(label, V, assigned_ind)
        elif isinstance(V, (int, ArraySizePlaceholder, Express)):
            V = to_pyqubo(V, placeholder=placeholder)
            index, index_set = _satisfied_index_set(label, list(range(V)), assigned_ind)
        elif isinstance(V, tuple):
            v0 = to_pyqubo(V[0], placeholder=placeholder)
            v1 = to_pyqubo(V[1], placeholder=placeholder)
            index, index_set = _satisfied_index_set(label, list(range(v0, v1)), assigned_ind)
        else:
            raise TypeError('index type is not {}'.format(type(V)))
        index_lists[index] = index_set

    indices_dict = []
    keys = list(index_lists.keys())
    num_indices = len(index_lists[keys[0]])
    for i in range(num_indices):
        ind_dict = {label: index_lists[label][i] for label in keys}
        ind_dict.update(assigned_ind)
        indices_dict.append(ind_dict)

    return indices_dict


def _satisfied_index_set(index_str: str, index_set:list, assigned: dict)->Tuple[str, list]:
    """index のkey文字列が i < j のような条件演算を含むとき, 条件を満たすsetを書き出してくる

    Args:
        index_str (str): [description]
        index_set (list): [description]
        assigned (dict): [description]

    Returns:
        Tuple[str, list]: [description]
    """
    ind_chars = index_str.split(' ')
    if len(ind_chars) == 1:
        return index_str, index_set

    index, operator, right_ind = ind_chars
    return index, [j for j in index_set if eval('{} {} {}'.format(j, operator, assigned[right_ind]))]
    




