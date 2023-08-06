import json
import requests
from typing import Tuple
import time

# import grpc
# import google.protobuf.wrappers_pb2
# from jijcloud.api import solver_pb2, solver_pb2_grpc


POST_SOLVER = {
    "hardware": str,
    "algorithm": str,
    "num_variables": int,
    "problem": dict,
    "problem_type": str,
    "parameters": dict,
    "info": dict
}

def post_instance(url: str, token: str, problem: dict)->dict:
    endpoint = url if url[-1] != '/' else url[:-1]
    endpoint += '/jijcloudpostinstance/JijCloudPostInstance/'
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": token
    }
    json_data = json.dumps(problem)
    res = requests.post(endpoint, headers=headers, data=json_data)

    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # TODO: set error logger
        if res.text != 'Internal Server Error':
            print('error object', res.json())
        raise requests.exceptions.HTTPError(e)

    return res.json()


def solver_api(url: str, token: str, parameters: dict, cachekey: str):
    endpoint = url if url[-1] != '/' else url[:-1]
    endpoint += '/solver/'
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": token
    }

    json_data = json.dumps({
        'instanceCacheKey': cachekey,
        'parameters': parameters
    })

    res = requests.post(endpoint, headers=headers, data=json_data)

    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # TODO: set error logger
        if res.text != 'Internal Server Error':
            print('error object', res.json())
        raise requests.exceptions.HTTPError(e)

    return res.json()


def fetch_api(url: str, token: str, cachekey: str):
    endpoint = url if url[-1] != '/' else url[:-1]
    endpoint += '/fetch/'
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": token
    }

    json_data = json.dumps({
        'cachekey': cachekey,
    })

    res = requests.post(endpoint, headers=headers, data=json_data)

    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # TODO: set error logger
        if res.text != 'Internal Server Error':
            print('error object', res.json())
        raise requests.exceptions.HTTPError(e)

    return res.json()



def post_to_solver(instance_url, solver_url, token, instance, parameters, sync:bool=True):
    # Instance を投げる
    instance_key = post_instance(instance_url, token, instance)

    # Solverにqueryをなげる
    solver_res = solver_api(solver_url, token, parameters, instance_key['cachekey'])

    # 同期モードで解を取得
    if sync:
        while True:
            response = fetch_api(solver_url, token, solver_res['cachekey'])
            if response['status'] == 'SUCCESS':
                break
    else:
        raise ValueError('only corresponds sync mode.')

    return json.loads(response['result'])
    




    



# def post_to_solver(url: str, token: str, body: dict, timeout: float) -> Tuple[int, dict]:
#     """Post to /solver endpoint

#     Args:
#         url (str): API URL which can be get Jij-Cloud-Web.
#         token (str): Token string.
#         body (dict): post dictionary.
#         timeout (float): number of timeout for post request.

#     Raises:
#         requests.exceptions.HTTPError: [description]

#     Returns:
#         (int, dict): status_code, response json as dict.
#     """
#     endpoint = url if url[-1] != '/' else url[:-1]
#     endpoint += '/solver/'
#     headers = {'Authorization': 'Bearer ' + token,
#                "Content-Type": "application/json"}

#     # validation -------------------------------
#     for k, v_type in POST_SOLVER.items():
#         if k not in body:
#             raise ValueError('body should have "{}".'.format(k))
#         if not isinstance(body[k], v_type):
#             raise TypeError('{} is type: "{}".'.format(k, v_type))
#     # ------------------------------- validation

#     json_data = json.dumps(body)
#     res = requests.post(endpoint, headers=headers,
#                         data=json_data, timeout=timeout)
#     res.raise_for_status()
#     data = res.json()
#     if 'error' in data:
#         message = res.json().get('error', res.text)
#         if isinstance(message, dict):
#             message = message['msg']
#         raise requests.exceptions.HTTPError(
#             str(res.status_code) + ' ' + message)

#     return res.status_code, res.json()


# def post_to_solver(url: str, token: str, body: dict, timeout: float, sync=True) -> Tuple[int, dict]:
#     """Post to solver gRPC endpoint
#     """
#     # Connect ot the VM via gRPC
#     post_keys = [
#         'num_variables', 'num_interactions', 'variable_labels',
#         'variable_type', 'linear_biases','quadratic_biases',
#         'quadratic_head', 'quadratic_tail'
#         ]
#     bqm = {k: body['problem'][k] for k in post_keys}
#     # encode list to str
#     bqm['variable_labels'] = json.dumps(bqm['variable_labels'])
#     if bqm['variable_type'] == 'SPIN':
#         bqm['variable_type'] = solver_pb2.BQM.BinaryType.SPIN
#     elif bqm['variable_type'] == 'BINARY':
#         bqm['variable_type'] == solver_pb2.BQM.BinaryType.BINARY

#     with grpc.insecure_channel(url) as channel:
#         stub = solver_pb2_grpc.JijSolverStub(channel)

#         problem = solver_pb2.Problem(bqm = solver_pb2.BQM(**bqm))

#         param_dict = {}
#         for k, v in body['parameters'].items():
#             if isinstance(v, float):
#                 param_dict[k] = google.protobuf.wrappers_pb2.DoubleValue(value=v)
#             elif isinstance(v, int):
#                 param_dict[k] = google.protobuf.wrappers_pb2.UInt64Value(value=v)
#             elif isinstance(v, str):
#                 param_dict[k] = google.protobuf.wrappers_pb2.StringValue(value=v)
#             elif isinstance(v, list) and k == 'schedule':
#                 # schedule setting
#                 if body['hardware'] == 'cpu' and body['algorithm'] == 'sa':   
#                     # sa schedule: [(0.1, 100), (0.5, 200), ...]
#                     param_dict[k] = [solver_pb2.SA.Schedule(beta=beta, one_mc_step=mc_step) for (beta,mc_step) in v]
#                 elif body['hardware'] == 'cpu' and body['algorithm'] == 'sqa':   
#                     # sqa schedule: [((0.1, 0.1), 100), ((0.1, 0.2), 200), ...]
#                     param_dict[k] = [solver_pb2.SQA.Schedule(tuple=solver_pb2.SQA.ParamTuple(beta=beta,s=s), one_mc_step=mc_step) for ((beta,s),mc_step) in v]
#                 elif body['hardware'] == 'gpu' and body['algorithm'] == 'sa':   
#                     # gpusa schedule: [(0.1, 100), (0.5, 200), ...]
#                     param_dict[k] = [solver_pb2.GPUSA.Schedule(beta=beta, one_mc_step=mc_step) for (beta,mc_step) in v]
#                 elif body['hardware'] == 'gpu' and body['algorithm'] == 'chimera-sa':   
#                     # gpu_chimera_sa schedule: [(0.1, 100), (0.5, 200), ...]
#                     param_dict[k] = [solver_pb2.GPUChimeraSA.Schedule(beta=beta, one_mc_step=mc_step) for (beta,mc_step) in v]
#                 elif body['hardware'] == 'gpu' and body['algorithm'] == 'chimera-sqa':   
#                     # gpu_chimera_sqa schedule: [(0.1, 100), (0.5, 200), ...]
#                     param_dict[k] = [solver_pb2.GPUChimeraSQA.Schedule(tuple=solver_pb2.GPUChimeraSQA.ParamTuple(beta=beta,s=s), one_mc_step=mc_step) for ((beta,s),mc_step) in v]

#         if body['hardware'] == 'cpu' and body['algorithm'] == 'sa':   
#             parameters = solver_pb2.Parameters(sa = solver_pb2.SA(**param_dict))
#         elif body['hardware'] == 'cpu' and body['algorithm'] == 'sqa':   
#             parameters = solver_pb2.Parameters(sqa = solver_pb2.SQA(**param_dict))
#         elif body['hardware'] == 'gpu' and body['algorithm'] == 'sa':   
#             parameters = solver_pb2.Parameters(gpu_sa = solver_pb2.GPUSA(**param_dict))
#         elif body['hardware'] == 'gpu' and body['algorithm'] == 'chimera-sa':   
#             parameters = solver_pb2.Parameters(gpu_chimera_sa = solver_pb2.GPUChimeraSA(**param_dict))
#         elif body['hardware'] == 'gpu' and body['algorithm'] == 'chimera-sqa':   
#             parameters = solver_pb2.Parameters(gpu_chimera_sqa = solver_pb2.GPUChimeraSQA(**param_dict))
#         else:
#             raise SolverError(body, 'Error')

#         probleminfo = solver_pb2.ProblemInfo(problem = problem, parameters = parameters)

#         # submit job to get cachekey
#         keyresponse = stub.submit_job(probleminfo)

#         # if the result is invalid, throw RuntimeException
#         if not keyresponse.status == solver_pb2.SUCCESS:
#             raise RuntimeError('cannot submit job: {}'.format(keyresponse.cachekey))

#         if sync:
#             while True:
#                 response, api_result = get_result(stub, keyresponse.cachekey)
#                 if not response.status == solver_pb2.PENDING:
#                     break
#                 time.sleep(1)
#         else:
#             response, api_result = get_result(stub, keyresponse.cachekey)
                
#         return 200, api_result

# def get_result(stub, cacheKey):
#     response = stub.fetch_result(solver_pb2.Cachekey(cachekey=cacheKey))
#     if not response.status == solver_pb2.PENDING:

#         # if status is failed, throw RuntimeError
#         if not response.status == solver_pb2.SUCCESS:
#             # job seems to be failed
#             raise RuntimeError('job failed: {}'.format(response.result))
#         else:
#             api_result = {
#                 'response': json.loads(response.result),
#                 'info': {
#                     'cachekey': cacheKey,
#                     'status': response.status
#                 }
#             }
#     else:
#         #pending
#         api_result = {
#             'response': {},
#             'info': {
#                 'cachekey': cacheKey,
#                 'status': response.status
#             }
#         }
#     return response, api_result


# class SolverError(Exception):
#     def __init__(self, body, message):
#         info = {
#             'hardware': body['hardware'],
#             'algorithm': body['algorithm'],
#             'problem_type': body['problem_type']
#         }
#         self.message = '{} is not supported in this version'.format(info)

#     def __str__(self):
#         return self.message

