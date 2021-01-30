from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DronesConfig(AppConfig):
    name = "apps.drones"
    verbose_name = _("Drones")

    def ready(self) -> None:
        from . import signals