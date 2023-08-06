from typing import List, Tuple, Union, Type

from jijcloud.modeling.variables.to_pyqubo import ToPyQUBO
from jijcloud.modeling.sum import Sum
from jijcloud.modeling.express import Express
from jijcloud.modeling.variables.binary import Binary


class Tensor(ToPyQUBO):

    def __init__(self, label: str, var_type: type, var_args: dict, shape: tuple, indices: List[str]):
        self.label = label
        self.var_type = var_type
        self.index_labels = indices
        self._var_args = var_args
        self.shape = (shape, ) if isinstance(shape, int) else shape


    def __repr__(self):
        index_str = ''
        for i in self.index_labels:
            index_str += '[%s]' % i
        return self.label + index_str

    def to_pyqubo(self, **indices):
        index_label = ''
        for label in self.index_labels:
            if not isinstance(label, str):
                index_label += '[%d]' % label
            else:
                index_label += '[%d]' % indices[label]
        variable = self.var_type(self.label+index_label, **self._var_args)
        return variable.to_pyqubo()


class Array:
    def __init__(self, var_type: type, label: str, shape: tuple, **kwargs):
        self.variable = var_type(label, **kwargs)
        self.var_type = var_type
        self.label = label
        self.shape = (shape, ) if isinstance(shape, int) else shape
        self.dim = len(self.shape)
        self.var_args = kwargs

    def to_pyqubo(self, fixed_variables: dict = {}):
        
        # check that variable can convert to pyqubo
        if not isinstance(self.variable, ToPyQUBO):
            raise ValueError("{} cannot convert to pyqubo object".format(self.variable.__class__.__name__))

    def __getitem__(self, key: Union[str, Tuple[str, ...]])->Type[Express]:
        if not isinstance(key, tuple):
            key = (key, )

        if len(key) != self.dim:
            raise ValueError("{}'s dimension is {}.".format(self.label, self.dim))

        indices = list(key)
        summation_index = []
        for i, k in enumerate(indices):
            # for syntaxsugar x[:]
            if isinstance(k, slice):
                indices[i] = '{}_slice'.format(i)
                summation_index.append((i, indices[i]))
            # elif isinstance(k, int):
                # TODO: repr の文字列変える. 整数添字の対応

        term = LeafTerm(Tensor(self.label, self.var_type, self.var_args, self.shape, indices))

        # for syntaxsugar x[:]
        for i, ind in summation_index:
            term = Sum({ind: self.shape[i]}, term)

        return term



def BinaryArray(label: str, shape: tuple):
    return Array(Binary, label, shape)



class LeafTerm(Express, ToPyQUBO):
    def __init__(self, child: Tensor):
        self.children = [child]
        if isinstance(child, Tensor):
            self.index_labels = child.index_labels
        else:
            self.index_labels = []

    def to_pyqubo(self, **indices):
        child = self.children[0]
        return child.to_pyqubo(**indices)