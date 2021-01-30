from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings

from .models import Drone


@receiver(post_save, sender=Drone)
def drone_save_handler(sender, **kwargs):
    if settings.DEBUG:
        print(f"{kwargs['instance']} saved.")


@receiver(post_delete, sender=Drone)
def drone_delete_handler(sender, **kwargs):
    if settings.DEBUG:
        print(f"{kwargs['instance']} deleted.")