import requests

from wafec.fi.hypothesis.exceptions import *

__all__ = [
    'ClientBase'
]

methods = {
    'post': requests.post,
    'get': requests.get,
    'put': requests.put,
    'delete': requests.delete
}


class ClientBase:
    def __init__(self, endpoint, prefix_route):
        self.endpoint = endpoint
        self.prefix_route = prefix_route
        self.response = None

    def request(self, path, method, data=None):
        method_func = methods[method.lower()]
        url = '{}{}{}'.format(self.endpoint, self.prefix_route, path)
        if data:
            self.response = method_func(url, data=data)
        else:
            self.response = method_func()
        if self.response.status_code < 400:
            content_type = self.response.headers.get('Content-Type')
            if content_type == 'application/json' and self.response.text:
                return self.response.json()
            return None
        elif self.response.status_code < 500:
            raise ClientErrorException('<ClientErrorException(status_code={})>'.format(self.response.status_code))
        elif self.response.status_code < 600:
            raise ServerErrorException('<ServerErrorException(status_code={})>'.format(self.response.status_code))
        else:
            raise ClientException('<ClientException(status_code={})>'.format(self.response.status_code))
