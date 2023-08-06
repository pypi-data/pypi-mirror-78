from jijcloud.modeling.variables.to_pyqubo import ToPyQUBO
from jijcloud.modeling.variables.variable import Variable
from jijcloud.modeling import Array
from jijcloud.modeling.variables.array import LeafTerm
import pyqubo
import numpy as np

def Placeholder(label):
    return LeafTerm(PlaceholderType(label))

class PlaceholderType(Variable, ToPyQUBO):

    def __init__(self, label, array=None) -> None:
        self.label = label
        self.array = array

    def to_pyqubo(self):
        if self.array is None:
            return pyqubo.Placeholder(self.label)
        else:
            label_parse = [int(s[:-1]) for s in self.label.split('[')[1:]]
            value = self.array[:]
            for ind in label_parse:
                value = value[ind]
            return value

def PlaceholderArray(label: str, array: np.ndarray):
    return Array(PlaceholderType, label, array.shape, array=array)