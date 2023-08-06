from sqlalchemy import *
from sqlalchemy.orm import relationship

from . import Base


class FITestParameterFaultExecution(Base):
    __tablename__ = 'test_parameter_fault_execution'

    id = Column(Integer, primary_key=True)
    test_parameter_fault_id = Column(Integer, ForeignKey('test_parameter_fault.id'))
    test_parameter_fault = relationship('FITestParameterFault')
    created_at = Column(DateTime)
    infection_succeed = Column(Boolean)
