from .base import ClientBase


class TestControllerClient(ClientBase):
    def __init__(self, endpoint):
        ClientBase.__init__(self, endpoint, '/api/tests')

    def create(self, uuid):
        result = self.request('', 'POST', data={'uuid': uuid})
        return result

    def as_last(self, uuid):
        result = self.request('', 'PUT', data={'uuid': uuid})
        return result
