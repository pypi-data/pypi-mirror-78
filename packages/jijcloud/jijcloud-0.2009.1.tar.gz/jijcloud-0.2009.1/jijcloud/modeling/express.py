from typing import List, Any, Union

from abc import ABCMeta

# from jijcloud.modeling.variables.array import Tensor
from jijcloud.modeling.variables.to_pyqubo import ToPyQUBO


class Express(metaclass=ABCMeta):
    def __init__(self, children: List[Any]):
        self.children = children
        index_labels = []
        for child in self.children:
            if isinstance(child, Express):
                index_labels += child.index_labels
        self.index_labels = list(set(index_labels))

    def __sub__(self, other):
        return self.__add__(-1*other)

    def __add__(self, other):
        return Add(self, other)

    def __mul__(self, other):
        return Mul(self, other)

    def __pow__(self, other):
        return Power(self, other)

    def __repr__(self):
        str_repr = ""
        for child in self.children:
            str_repr +=  child.__repr__() + " "
        return str_repr[:-1]


    def to_pyqubo(self):
        return self.children[0].to_pyqubo()


TermType = Union[Express, int, float]
        

class Add(Express, ToPyQUBO):
    def __init__(self, *terms: TermType):
        super().__init__(list(terms))

    def __repr__(self):
        str_repr = ""
        for t in self.children:
            str_repr += t.__repr__() + ' + '
        return str_repr[:-3]

    def to_pyqubo(self, **indices):
        def pyqubo(term):
            if isinstance(term, ToPyQUBO):
                return term.to_pyqubo(**indices)
            else:
                return term
        return sum(pyqubo(child) for child in self.children)

class Mul(Express, ToPyQUBO):
    def __init__(self, *terms: TermType):
        super().__init__(list(terms))

    def __repr__(self):
        str_repr = ""
        for t in self.children:
            if isinstance(t, Add) and len(t.children) > 1:
                str_repr += '(%s)' % t.__repr__()
            else:
                str_repr += t.__repr__()
        return str_repr

    def to_pyqubo(self, **indices):
        term = 1
        for child in self.children:
            term *= child.to_pyqubo(**indices) if isinstance(child, ToPyQUBO) else child
        return term

class Power(Express, ToPyQUBO):
    def __init__(self, base: TermType, exponent: int):
        super().__init__([base, exponent])
        self.base = base
        self.exponent = exponent

    def to_pyqubo(self, **indices):
        term = self.base.to_pyqubo(**indices)
        return term ** self.exponent