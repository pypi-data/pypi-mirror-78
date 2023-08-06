from datetime import datetime

from wafec.fi.hypothesis.models import *
from .base import ServiceBase


class TestService(ServiceBase):
    def get_last_test(self):
        test = self.db_session.query(FITest).order_by(FITest.updated_at.desc()).first()
        return test

    def create(self, uuid):
        test = self.get(uuid)
        if not test:
            test = FITest()
            test.uuid = uuid
            test.created_at = datetime.now()
            test.updated_at = datetime.now()
            self.db_session.add(test)
        return test

    def as_last(self, uuid):
        test = self.get(uuid)
        if test:
            test.updated_at = datetime.now()
        return test

    def get(self, uuid):
        test = self.db_session.query(FITest).filter_by(uuid=uuid).one_or_none()
        return test
