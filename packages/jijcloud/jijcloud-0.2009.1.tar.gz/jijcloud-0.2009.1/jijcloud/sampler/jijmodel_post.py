import dimod
from abc import ABCMeta
from typing import Dict, Union
from numbers import Number
import numpy as np
import json

from requests.api import post
from jijcloud.post_api import post_to_solver
from jijmodeling.express.express import Express


class JijModelingInterface(metaclass=ABCMeta):
    def sample_model(self, 
        model: Express, 
        feed_dict: Dict[str, Union[Number, list, np.ndarray]],
        multipliers: Dict[str, Number], 
        search: bool = False,
        timeout=None,
        **kwargs):

        m_seri = model.to_serializable()

        parameters = kwargs
        parameters['multipliers'] = multipliers
        parameters['mul_search'] = search

        response = post_to_solver(
            instance_url=self.url.instance_url,
            solver_url=self.url.solver_url,
            token =self.token,
            instance={
                'problem_type': 'JijMathModel',
                'model': {
                    'mathematical_model': json.dumps(m_seri),
                    'instance_data': feed_dict
                }
            },
            parameters = parameters
        )

        sample_set = dimod.SampleSet.from_serializable(response)
        return sample_set
