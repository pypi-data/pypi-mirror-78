from . import app, api
from . import TestController, TestParameterController


api.add_resource(TestController, '/api/tests')
api.add_resource(TestParameterController, '/api/parameters')
