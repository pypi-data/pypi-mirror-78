from sqlalchemy import *
from sqlalchemy.orm import relationship

from . import Base


class FITestParameter(Base):
    __tablename__ = 'test_parameter'

    id = Column(Integer, primary_key=True)
    test_id = Column(Integer, ForeignKey('test.id'))
    test = relationship('FITest')
    name = Column(String)
    test_parameter_service_id = Column(Integer, ForeignKey('test_parameter_service.id'))
    test_parameter_service = relationship('FITestParameterService')
    test_parameter_context_id = Column(Integer, ForeignKey('test_parameter_context.id'))
    test_parameter_context = relationship('FITestParameterContext')
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    updated_count = Column(Integer)
