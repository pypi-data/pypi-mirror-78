from datetime import datetime

from .base import ServiceBase
from wafec.fi.hypothesis.models import *
from .test_service import TestService
from wafec.fi.hypothesis.exceptions import NotFoundException

from sqlalchemy import and_


class ParameterService(ServiceBase):
    def __init__(self):
        ServiceBase.__init__(self)
        self.test_service = TestService()

    def create_service_if_not_exists(self, service):
        service_instance = self.db_session.query(FITestParameterService).filter_by(service_name=service).one_or_none()
        if not service_instance:
            service_instance = FITestParameterService()
            service_instance.service_name = service
            self.db_session.add(service_instance)
        return service_instance

    def create_context_if_not_exists(self, context):
        context_instance = self.db_session.query(FITestParameterContext).filter_by(context_label=context).one_or_none()
        if not context_instance:
            context_instance = FITestParameterContext()
            context_instance.context_label = context
            self.db_session.add(context_instance)
        return context_instance

    def create(self, name, service, context):
        test_last = self.test_service.get_last_test()
        if not test_last:
            raise NotFoundException('No test found')
        parameter_instance = None
        service_instance = self.db_session.query(FITestParameterService).filter_by(service_name=service).one_or_none()
        context_instance = self.db_session.query(FITestParameterContext).filter_by(context_label=context).one_or_none()
        if service_instance and context_instance:
            parameter_instance = self.db_session.query(FITestParameter).filter(
                and_(FITestParameter.name == name,
                     FITestParameter.test_id == test_last.id,
                     FITestParameter.test_parameter_service_id == service_instance.id,
                     FITestParameter.test_parameter_context_id == context_instance.id)).one_or_none()
        if not parameter_instance:
            if not service_instance:
                service_instance = self.create_service_if_not_exists(service)
            if not context_instance:
                context_instance = self.create_context_if_not_exists(context)
            parameter_instance = FITestParameter()
            parameter_instance.name = name
            parameter_instance.test = test_last
            parameter_instance.test_parameter_service = service_instance
            parameter_instance.test_parameter_context = context_instance
            parameter_instance.created_at = datetime.now()
            parameter_instance.updated_at = datetime.now()
            parameter_instance.updated_count = 1
            self.db_session.add(parameter_instance)
        else:
            updated_count = parameter_instance.updated_count if parameter_instance.updated_count else 1
            parameter_instance.updated_count = updated_count + 1
            parameter_instance.updated_at = datetime.now()
        return parameter_instance
