from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from django_fastadmin.models import SimpleTask
from django_fastadmin.widgets import AceWidget
from django_readedit_switch_admin.admin import DjangoReadEditSwitchAdmin

from . import settings


class SmtpServerForm(forms.ModelForm):
    class Meta:
        fields = "__all__"
        widgets = {
            "options_raw": AceWidget(ace_options={
                "mode": "ace/mode/yaml",
                "theme": "ace/theme/twilight",
            })
        }

class SmtpServerAdmin(DjangoReadEditSwitchAdmin, admin.ModelAdmin):
    form = SmtpServerForm
    list_display = ["name", "code", "enable", "options_can_be_parsed"]
    list_filter = ["enable"]
    search_fields = ["name", "code"]
    readonly_fields = ["enable_time", "disable_time"]


class TemplateForm(forms.ModelForm):
    class Meta:
        fields = "__all__"
        widgets = {
            "body": AceWidget(ace_options={
                "mode": "ace/mode/html",
                "theme": "ace/theme/twilight",
            })
        }
class TemplateAdmin(DjangoReadEditSwitchAdmin, admin.ModelAdmin):
    form = TemplateForm
    list_display = ["name", "code", "enable"]
    list_filter = ["enable"]
    search_fields = ["name", "code", "subject", "body"]
    readonly_fields = ["enable_time", "disable_time"]


class AttachmentOfMailForDeliveryInline(admin.TabularInline):
    extra = 0

class MailForDeliveryAdmin(DjangoReadEditSwitchAdmin, admin.ModelAdmin):
    list_display = ["subject", "status", "server", "template", "add_time", "mod_time"]
    list_filter = ["status"]
    search_fields = ["subject", "body", "template", "variables_raw", "sender", "recipient", "result", "error_code", "error_message"]
    fieldsets = [
        (None, {
            "fields": ["server", "sender", "recipient", "subject", "body", "template", "variables_raw"],
        }),
        (_("Simple Task Information"), {
            "fields": SimpleTask.SIMPLE_TASK_FIELDS,
        })
    ]
    readonly_fields = [] + SimpleTask.SIMPLE_TASK_FIELDS
    inlines = [
        AttachmentOfMailForDeliveryInline,
    ]
    actions = [
        "action_reset_mail_status",
    ]

    def action_reset_mail_status(self, request, queryset):
        for mail in queryset:
            mail.reset(save=True)
    action_reset_mail_status.short_description = _("Reset Mail Status")
    action_reset_mail_status.allowed_permissions = ["reset_mail_status"]

    def has_reset_mail_status_permission(self, reqeust):
        app_label = self.model._meta.app_label
        return reqeust.user.has_perm("{}.reset_mail_status".format(app_label))


if settings.DJANGO_MAILCENTER_AUTO_REGISTER_ADMINS and settings.DJANGO_MAILCENTER_AUTO_REGISTER_MODELS:
    from .models import SmtpServer
    from .models import Template
    from .models import MailForDelivery
    from .models import AttachmentOfMailForDelivery

    SmtpServerForm.model = SmtpServer
    TemplateForm.model = Template
    AttachmentOfMailForDeliveryInline.model = AttachmentOfMailForDelivery

    admin.site.register(SmtpServer, SmtpServerAdmin)
    admin.site.register(Template, TemplateAdmin)
    admin.site.register(MailForDelivery, MailForDeliveryAdmin)
