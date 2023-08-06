from .base import ClientBase


class ParameterControllerClient(ClientBase):
    def __init__(self, endpoint):
        ClientBase.__init__(self, endpoint, '/api/parameters')

    def create_or_update(self, name, service, context):
        result = self.request('', 'POST', data={'name': name, 'service_name': service, 'context_label': context})
        return result
