from django.urls import path
from django.urls import include
from .models import Mail

urlpatterns = [
    path('mailcenter/mailjob/', include(Mail.get_services().get_urls()),
]