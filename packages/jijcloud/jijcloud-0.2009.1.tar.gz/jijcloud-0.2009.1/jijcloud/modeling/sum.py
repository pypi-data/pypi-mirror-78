from typing import List, Union, Tuple

import numpy as np
import pyqubo
from jijcloud.modeling.express import Express
from jijcloud.modeling.variables.to_pyqubo import ToPyQUBO


class Sum(Express, ToPyQUBO):
    def __init__(self, indices: dict, term: Express):
        super().__init__(children=[term])
        self.indices = indices

        index_keys = list(indices.keys())
        self.index_labels = [ind for ind in self.index_labels if ind not in index_keys]

    def to_pyqubo(self, **indices)->Union[int, float, pyqubo.Express]:
        term = self.children[0]
        sum_index = _reshape_to_index_set(self.indices, indices)
        return sum(term.to_pyqubo(**ind) for ind in sum_index)

    def __repr__(self):
        repr_str = 'Σ_{'
        for i in self.indices.keys():
            repr_str += i + ', '
        term = self.children[0]
        repr_str = repr_str[:-2] + '}}({})'.format(term.__repr__()) 
        return repr_str







def _reshape_to_index_set(indices: dict, assigned_ind: dict)->List[dict]:
    index_lists = {}
    for label, V in indices.items():
        if isinstance(V, (list, np.ndarray)):
            index, index_set = _satisfied_index_set(label, V, assigned_ind)
        elif isinstance(V, int):
            index, index_set = _satisfied_index_set(label, list(range(V)), assigned_ind)
        elif isinstance(V, tuple):
            index, index_set = _satisfied_index_set(label, list(range(V[0], V[1])), assigned_ind)
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
    ind_chars = index_str.split(' ')
    if len(ind_chars) == 1:
        return index_str, index_set

    index, operator, right_ind = ind_chars
    return index, [j for j in index_set if eval('{} {} {}'.format(j, operator, assigned[right_ind]))]
    




