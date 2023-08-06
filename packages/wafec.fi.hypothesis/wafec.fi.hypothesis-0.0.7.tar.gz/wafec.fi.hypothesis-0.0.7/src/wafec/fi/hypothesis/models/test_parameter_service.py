from sqlalchemy import *

from . import Base


class FITestParameterService(Base):
    __tablename__ = 'test_parameter_service'

    id = Column(Integer, primary_key=True)
    service_name = Column(String)
