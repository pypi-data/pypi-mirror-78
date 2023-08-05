import yaml

from django.db import models
from django.template import Template as DjangoTemplate
from django.template import Context as DjangoContext
from django.utils.translation import ugettext_lazy as _

from sendmail import sendmail

from django_safe_fields.fields import SafeTextField
from django_safe_fields.fields import SafeCharField
from django_fastadmin.models import SimpleTask

from . import settings


class SmtpServer(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name=_("Name"))
    code = models.CharField(max_length=64, unique=True, verbose_name=_("Code"))
    is_failback_server = models.BooleanField(default=False, verbose_name=_("Failback Server"))
    order = models.IntegerField(default=1000, verbose_name=_("Order"))
    enable = models.BooleanField(verbose_name=_("Enable"))
    enable_time = models.DateTimeField(null=True, blank=True, verbose_name=_("Enabled Time"))
    disable_time = models.DateTimeField(null=True, blank=True, verbose_name=_("Disabled Time"))
    add_time = models.DateTimeField(auto_now_add=True, verbose_name=_("Add Time"))
    mod_time = models.DateTimeField(auto_now=True, verbose_name=_("Modify Time"))
    sender = SafeCharField(max_length=256, null=True, blank=True, verbose_name=_("Sender"))
    options_raw = SafeTextField(null=True, blank=True, verbose_name=_("Smtp Server Options"))

    class Meta:
        app_label = settings.DJANGO_MAILCENTER_APP_LABEL
        verbose_name = _("Smtp Server")
        verbose_name_plural = _("Smtp Servers")

    def __str__(self):
        return self.name

    @property
    def options(self):
        if not self.options_raw:
            return {}
        try:
            return yaml.safe_load(self.options_raw)
        except ValueError:
            return {}

    def options_can_be_parsed(self):
        if not self.options_raw:
            return None
        try:
            yaml.safe_load(self.options_raw)
            return True
        except ValueError:
            return False
    options_can_be_parsed.boolean = True
    options_can_be_parsed.short_description = _("Options Can Be Parsed")

    @classmethod
    def get_failback_server(cls):
        servers = cls.objects.filter(enable=True).filter(is_failback_server=True).order_by("order")[:1]
        if len(servers):
            return servers[0]
        else:
            return None

class Template(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name=_("Name"))
    code = models.CharField(max_length=64, unique=True, verbose_name=_("Code"))
    enable = models.BooleanField(verbose_name=_("Enable"))
    enable_time = models.DateTimeField(null=True, blank=True, verbose_name=_("Enabled Time"))
    disable_time = models.DateTimeField(null=True, blank=True, verbose_name=_("Disabled Time"))
    add_time = models.DateTimeField(auto_now_add=True, verbose_name=_("Add Time"))
    mod_time = models.DateTimeField(auto_now=True, verbose_name=_("Modify Time"))
    subject = models.CharField(max_length=256, null=True, blank=True, verbose_name=_("Subject"))
    body = models.TextField(null=True, blank=True, verbose_name=_("Body"))

    class Meta:
        app_label = settings.DJANGO_MAILCENTER_APP_LABEL
        verbose_name = _("Mail Template")
        verbose_name_plural = _("Mail Templates")

    def __str__(self):
        return self.name

    @classmethod
    def template_render(cls, template, variables):
        t = DjangoTemplate(template)
        c = DjangoContext(variables)
        return t.render(c)

    def render_subject(self, variables=None):
        variables = variables or {}
        return self.template_render(self.subject, variables)

    def render_body(self, variables=None):
        variables = variables or {}
        return self.template_render(self.body, variables)

class MailForDelivery(SimpleTask):
    server = models.ForeignKey(SmtpServer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Smtp Server"))
    subject = models.CharField(max_length=512, verbose_name=_("Subject"))
    body = models.TextField(null=True, blank=True, verbose_name=_("Body"))
    template = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Mail Template"))
    variables_raw = models.TextField(null=True, blank=True, verbose_name=_("Variables"))
    sender = SafeCharField(max_length=1024, null=True, blank=True, verbose_name=_("Sender"))
    recipient = SafeCharField(max_length=1024, verbose_name=_("Recipient"))

    class Meta:
        app_label = settings.DJANGO_MAILCENTER_APP_LABEL
        verbose_name = _("Mail For Delivery")
        verbose_name_plural = _("Mails ForDelivery")

    def __str__(self):
        return self.subject

    def get_variables_raw(self):
        if not self.variables_raw:
            return {}
        try:
            return yaml.safe_load(self.variables_raw)
        except ValueError:
            return {}
    
    def set_variables_raw(self, value):
        self.variables_raw = yaml.safe_dump(value)
    
    variables = property(get_variables_raw, set_variables_raw)

    def get_body(self):
        if self.template:
            return self.template.render_body(self.variables)
        else:
            return self.body

    def get_subject(self):
        if self.template:
            return self.template.render_subject(self.variables)
        else:
            return self.subject

    def get_attachment_files(self):
        files = []
        for attachment in self.attachments.all():
            filename= attachment.file.path
            files.append(filename)
        return files

    def do_task_main(self):
        print("Send mail: {}".format(self.get_subject()))
        server = self.server or SmtpServer.get_failback_server()
        sender = self.sender or server.sender
        sendmail(sender, [self.recipient], self.get_body(), self.get_subject(), self.get_attachment_files(), True, **server.options)

class AttachmentOfMailForDelivery(models.Model):
    mail = models.ForeignKey(MailForDelivery, on_delete=models.CASCADE, related_name="attachments", verbose_name=_("Mail"))
    file = models.FileField(upload_to="django-mailcenter/MailForDelivery/Attachments/", verbose_name=_("File"))
    filename = models.CharField(max_length=256, null=True, blank=True, verbose_name=_("Filename"))

    class Meta:
        app_label = settings.DJANGO_MAILCENTER_APP_LABEL
        verbose_name = _("Attachment Of Mail For Delivery")
        verbose_name_plural = _("Attachments Of Mail For Delivery")

    def __str__(self):
        return self.filename
