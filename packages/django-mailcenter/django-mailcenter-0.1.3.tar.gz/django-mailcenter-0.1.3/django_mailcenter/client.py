from . import settings


class DjangoMailcenterClient(object):
    def __init__(self, service):
        self.service = service
    
    def send_template_mail(self, server_code, template_code, variables, recipient):
        return self.service.send_template_mail(server_code, template_code, variables, recipient)


class DjangoMailcenterRemoteService(object):
    
    def __init__(self, api_server):
        self.api_server = api_server

    def send_template_mail(self, server_code, template_code, variables, recipient):
        raise NotImplementedError()


def get_default_mailcenter_client():
    if settings.DJANGO_MAILCENTER_AUTO_REGISTER_MODELS:
        from .services import django_mailcenter_service
        return DjangoMailcenterClient(django_mailcenter_service)
    else:
        if not settings.DJANGO_MAILCETNER_API_SERVER:
            raise RuntimeError("You must set DJANGO_MAILCETNER_API_SERVER in settings.py.")
        return DjangoMailcenterClient(DjangoMailcenterRemoteService(settings.DJANGO_MAILCETNER_API_SERVER))
