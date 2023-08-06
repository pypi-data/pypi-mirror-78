from . import app, api
from . import TestController, TestParameterController

from threading import Lock

TEST_PARAMETER_LOCK = Lock()

api.add_resource(TestController, '/api/tests')
api.add_resource(TestParameterController, '/api/parameters',
                 resource_class_kwargs ={'lock_obj': TEST_PARAMETER_LOCK})
