from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from django_fastadmin.widgets import AceWidget

from .models import SmtpServer
from .models import Template
from .models import MailForDelivery
from .models import AttachmentOfMailForDelivery


class SmtpServerForm(forms.ModelForm):
    class Meta:
        model = SmtpServer
        fields = "__all__"
        widgets = {
            "options_raw": AceWidget(ace_options={
                "mode": "ace/mode/yaml",
                "theme": "ace/theme/twilight",
            })
        }

class SmtpServerAdmin(admin.ModelAdmin):
    form = SmtpServerForm
    list_display = ["name", "code", "enable", "options_can_be_parsed"]
    list_filter = ["enable"]
    search_fields = ["name", "code"]
    readonly_fields = ["enable_time", "disable_time"]


class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = "__all__"
        widgets = {
            "body": AceWidget(ace_options={
                "mode": "ace/mode/html",
                "theme": "ace/theme/twilight",
            })
        }
class TemplateAdmin(admin.ModelAdmin):
    form = TemplateForm
    list_display = ["name", "code", "enable"]
    list_filter = ["enable"]
    search_fields = ["name", "code", "subject", "body"]
    readonly_fields = ["enable_time", "disable_time"]


class AttachmentOfMailForDeliveryInline(admin.TabularInline):
    model = AttachmentOfMailForDelivery
    extra = 0

class MailForDeliveryAdmin(admin.ModelAdmin):
    list_display = ["subject", "status", "server", "template", "add_time", "mod_time"]
    list_filter = ["status"]
    search_fields = ["subject", "body", "template", "variables_raw", "sender", "recipient", "result", "error_code", "error_message"]
    fieldsets = [
        (None, {
            "fields": ["server", "sender", "recipient", "subject", "body", "template", "variables_raw"],
        }),
        (_("Simple Task Information"), {
            "fields": MailForDelivery.SIMPLE_TASK_FIELDS,
        })
    ]
    readonly_fields = [] + MailForDelivery.SIMPLE_TASK_FIELDS
    inlines = [
        AttachmentOfMailForDeliveryInline,
    ]

admin.site.register(SmtpServer, SmtpServerAdmin)
admin.site.register(Template, TemplateAdmin)
admin.site.register(MailForDelivery, MailForDeliveryAdmin)
