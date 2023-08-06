from sqlalchemy import *

from . import Base


class FITest(Base):
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True)
    uuid = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __repr__(self):
        return '<FITest(id={}, uuid={}, created_at={})>'.format(self.id, self.uuid, self.created_at)