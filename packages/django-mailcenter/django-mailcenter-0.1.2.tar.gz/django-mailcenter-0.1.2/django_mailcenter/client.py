from .models import MailForDelivery
from .models import SmtpServer
from .models import Template




def send_template_mail(server_code, template_code, variables, recipient):
    server = SmtpServer.objects.get(code=server_code)
    template = Template.objects.get(code=template_code)
    subject = template.render_subject(variables)

    mail = MailForDelivery()
    mail.server = server
    mail.subject = template.render_subject(variables)
    mail.template = template
    mail.variables = variables
    mail.recipient = recipient
    mail.save()

    return mail
