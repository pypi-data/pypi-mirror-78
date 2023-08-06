import dimod
from typing import Union
from jijcloud.post_api import post_to_solver
from jijcloud.setting import load_config
# from jijcloud import api

import json


class UrlPattern:
    def __init__(self, url: Union[str, dict]):
        if isinstance(url, dict):
            self.instance_url = url['instance_url']
            self.solver_url = url['solver_url']
        elif isinstance(url, str):
            self.instance_url, self.solver_url = url, url
        else:
            raise ValueError('needs url in config file')


class JijCloudSampler(dimod.Sampler):
    """JijCloudSampler
    another Sampler is based on this class
    """

    hardware = ''
    algorithm = ''

    def __init__(self, token=None, url=None, timeout=None, config=None, config_env='default'):
        """setting token and url

        Args:
            token (str, optional): token string. Defaults to None.
            url (str, optional): API URL. Defaults to None.
            timeout (float, optional): timeout for post request. Defaults to None.
            config (str, optional): Config file path. Defaults to None.

        Raises:
            TypeError: token, url, config is not str
        """

        if isinstance(config, str):
            _config = load_config(config)[config_env]
            self.token = _config['token']
            if 'url' in _config:
                self.url = UrlPattern(_config['url'])
            else:
                self.url = UrlPattern({k: _config[k] for k in ['instance_url', 'solver_url']})
            self.timeout = _config.get('timeout', 1)
        elif isinstance(token, str) and isinstance(url, (type(None), str, dict)):
            self.token = token
            if not url:
                # default url
                self.url = UrlPattern('default url')
            else:
                self.url = UrlPattern(url)
        else:
            raise ValueError('need config file or token and url')

        self.timeout = timeout if timeout is not None else 1
       

    def sample(self, bqm, num_reads=1, num_sweeps=100, timeout=None, sync=True, **kwargs):
        parameters = {'num_reads': num_reads, 'num_sweeps': num_sweeps}

        parameters.update(kwargs)
        # post_body = {
        #     'hardware': self.hardware,
        #     'algorithm': self.algorithm,
        #     # 'num_variables': bqm.num_variables,
        #     'problem_type': 'BinaryQuadraticModel',
        #     'problem': bqm.to_serializable(),
        #     'parameters': parameters,
        #     'info': {}
        # }

        # if timeout is defined in script, use this value
        if timeout:
            self.timeout = timeout

        instance = {
            'problem_type': 'BQM',
            'model': bqm.to_serializable()
        }

        response = post_to_solver(self.url.instance_url, self.url.solver_url, self.token, instance=instance, parameters=parameters, sync=sync)
        sample_set = dimod.SampleSet.from_serializable(response)

        return sample_set

    @property
    def properties(self):
        return dict()

    @property
    def parameters(self):
        return dict()

# import grpc
# import google.protobuf.wrappers_pb2
# from jijcloud.api import solver_pb2, solver_pb2_grpc
# from dimod.utilities import LockableDict
# class SampleSet(dimod.SampleSet):

#     def __init__(self, record, variables, info, vartype):
#         if not (record is None or variables is None or info is None or vartype is None):
#             super().__init__(record, variables, info, vartype)
#         else:
#             # empty data
#             self._record = None
#             self._variables = None
#             self._info = LockableDict({})
#             self._vartype = None

#     @property
#     def status(self):
#         if 'status' in self.info:
#             return self.info['status']
#         else:
#             return 'UNKNOWN'

#     def get_result(self, config, config_env='default'):

#         if self.status == api.SUCCESS:
#             return self

#         _config = load_config(config)[config_env]
#         url = _config['url']
#         with grpc.insecure_channel(url) as channel:
#             stub = solver_pb2_grpc.JijSolverStub(channel)
#             response = stub.fetch_result(solver_pb2.Cachekey(cachekey=self.info['cachekey']))

#         sample_set = SampleSet.from_serializable(json.loads(response.result))
#         return sample_set

