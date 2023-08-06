from wafec.fi.hypothesis.clients import ParameterControllerClient
from .configuration import Default


def parameter_client_factory():
    endpoint = Default.endpoint
    return ParameterControllerClient(endpoint)
