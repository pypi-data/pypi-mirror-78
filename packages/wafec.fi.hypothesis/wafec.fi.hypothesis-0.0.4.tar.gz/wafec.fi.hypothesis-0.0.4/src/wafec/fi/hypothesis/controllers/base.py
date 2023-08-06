from flask_restful import Resource

from wafec.fi.hypothesis.models import db_session


class ControllerBase(Resource):
    def __init__(self):
        Resource.__init__(self)
        self.db_session = db_session()
