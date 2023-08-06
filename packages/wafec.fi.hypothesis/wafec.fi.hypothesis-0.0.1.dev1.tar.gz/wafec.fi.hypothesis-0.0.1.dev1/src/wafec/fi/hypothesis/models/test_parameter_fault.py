from sqlalchemy import *
from sqlalchemy.orm import relationship

from . import Base


class FITestParameterFault(Base):
    __tablename__ = 'test_parameter_fault'

    id = Column(Integer, primary_key=True)
    test_parameter_id = Column(Integer, ForeignKey('test_parameter.id'))
    test_parameter = relationship('FITestParameter')
    fault_value = Column(String)