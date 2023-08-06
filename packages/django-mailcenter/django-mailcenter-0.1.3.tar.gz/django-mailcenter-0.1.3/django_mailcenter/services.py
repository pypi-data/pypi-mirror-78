from . import settings

class DjangoMailcenterService(object):
    def __init__(self, smtp_server_model, template_model, mail_for_delivery_model, attachment_of_mail_for_delivery_model):
        self.smtp_server_model = smtp_server_model
        self.template_model = template_model
        self.mail_for_delivery_model = mail_for_delivery_model
        self.attachment_of_mail_for_delivery_model = attachment_of_mail_for_delivery_model
    
    def send_template_mail(self, server_code, template_code, variables, recipient):
        server = self.smtp_server_model.objects.get(code=server_code)
        template = self.template_model.objects.get(code=template_code)
        subject = template.render_subject(variables)

        mail = self.mail_for_delivery_model()
        mail.server = server
        mail.subject = template.render_subject(variables)
        mail.template = template
        mail.variables = variables
        mail.recipient = recipient
        mail.save()

        return mail


if settings.DJANGO_MAILCENTER_AUTO_REGISTER_MODELS:
    from .models import SmtpServer
    from .models import Template
    from .models import MailForDelivery
    from .models import AttachmentOfMailForDelivery
    django_mailcenter_service = DjangoMailcenterService(SmtpServer, Template, MailForDelivery, AttachmentOfMailForDelivery)
