from sqlalchemy import *

from . import Base


class FITestParameterContext(Base):
    __tablename__ = 'test_parameter_context'

    id = Column(Integer, primary_key=True)
    context_label = Column(String)
