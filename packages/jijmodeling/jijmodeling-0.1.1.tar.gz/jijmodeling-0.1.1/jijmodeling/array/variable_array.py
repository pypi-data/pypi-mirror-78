from typing import Union, Tuple

from jijmodeling.variables import Binary, DisNum, Placeholder
from jijmodeling.array.array import Array, ArraySizePlaceholder

ShapeType = Union[int, ArraySizePlaceholder, Tuple[Union[int, ArraySizePlaceholder], ...]]

def BinaryArray(label: str, shape: ShapeType):
    return Array(Binary(label), shape)


def DisNumArray(label: str, shape: ShapeType, lower: float=0.0, upper: float=1.0, bits: int=3):
    return Array(DisNum(label, lower, upper, bits), shape)


def PlaceholderArray(label: str, shape: ShapeType=None, dim: int=None):
    if shape is None and isinstance(dim, int):
        # _shape = tuple([ArraySizePlaceholder(label=label + '_shape_%d' % i) for i in range(dim)])
        # array = Array(Placeholder(label), _shape)
        # for i, s in enumerate(_shape):
        #     s.set_array(array, i)
        _shape = tuple(None for _ in range(dim))
        return Array(Placeholder(label), _shape)
        return array
    elif shape is not None:
        shape = (shape, ) if isinstance(shape, int) else shape
        return Array(Placeholder(label), shape)
    else:
        raise ValueError("Input shape or dim.")
    
