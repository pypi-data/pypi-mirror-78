from .base import ControllerBase
from wafec.fi.hypothesis.services import ParameterService

from flask_restful import reqparse


class TestParameterController(ControllerBase):
    def __init__(self, lock_obj):
        ControllerBase.__init__(self)
        self._lock_obj = lock_obj
        self.parameter_service = ParameterService()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('service_name', type=str, required=True)
        parser.add_argument('context_label', type=str, required=True)
        args = parser.parse_args()
        with self._lock_obj:
            test_parameter = self.parameter_service.create(args['name'], args['service_name'], args['context_label'])
            self.db_session.commit()
            return {'id': test_parameter.id}, 201
