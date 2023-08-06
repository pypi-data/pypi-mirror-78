from wafec.fi.hypothesis.models import db_session


class ServiceBase:
    def __init__(self):
        self.db_session = db_session()
