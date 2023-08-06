from flask_restful import reqparse

from .base import ControllerBase
from wafec.fi.hypothesis.services import TestService

__all__ = [
    "TestController"
]


class TestController(ControllerBase):
    def __init__(self):
        ControllerBase.__init__(self)
        self.test_service = TestService()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uuid', type=str, help='Test Universal Unique Identifier', required=True)
        args = parser.parse_args()
        test = self.test_service.create(args['uuid'])
        self.db_session.commit()
        return {'id': test.id}, 201

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uuid', type=str, required=True)
        args = parser.parse_args()
        test = self.test_service.as_last(args['uuid'])
        self.db_session.flush()
        return {'id': test.id}, 201
