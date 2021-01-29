from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuthenticationConfig(AppConfig):
    name = "apps.authentication"  # defines the module of the current app
    verbose_name = _("Authentication")
