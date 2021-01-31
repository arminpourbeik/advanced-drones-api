import os
import contextlib
import uuid

from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from apps.core.models import CreationModificationDateBase


class DroneCategory(CreationModificationDateBase):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        max_length=255,
        unique=True,
    )

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Drone Categories"

    def __str__(self) -> str:
        return self.name


def drone_upload_to(instance, filename):
    base, extention = os.path.splitext(filename)
    extention = extention.lower()

    return f"drones/{instance.name}{extention}"


def pilot_upload_to(instance, filename):
    base, extention = os.path.splitext(filename)
    extention = extention.lower()

    return f"pilots/{instance.name}{extention}"


class Drone(CreationModificationDateBase):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    picture = models.ImageField(default="drone.png", upload_to=drone_upload_to)
    picture_thumbnail = ImageSpecField(
        source="picture",
        processors=[ResizeToFill(728, 250)],
        format="PNG",
    )
    category = models.ForeignKey(
        to=DroneCategory,
        related_name="drones",
        on_delete=models.CASCADE,
    )
    has_it_competed = models.BooleanField(default=False)
    owner = models.ForeignKey(
        to=get_user_model(),
        related_name="drones",
        on_delete=models.CASCADE,
    )
    manufacturing_date = models.DateTimeField()

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name

    def delete(self, *args, **kwargs):
        from django.core.files.storage import default_storage

        if self.picture:
            with contextlib.suppress(FileNotFoundError):
                default_storage.delete(self.picture_thumbnail.path)
            self.picture.delete()
        super().delete(*args, **kwargs)


class Pilot(CreationModificationDateBase):
    MALE = "M"
    FEMALE = "F"
    GENDER_CHOICES = (
        (MALE, "Male"),
        (FEMALE, "Female"),
    )
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250, blank=False, unique=True)
    picture = models.ImageField(default="drone.png", upload_to=pilot_upload_to)
    picture_thumbnail = ImageSpecField(
        source="picture",
        processors=[ResizeToFill(728, 250)],
        format="PNG",
    )
    gender = models.CharField(
        max_length=2,
        choices=GENDER_CHOICES,
        default=MALE,
    )
    races_count = models.IntegerField()

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name

    def delete(self, *args, **kwargs):
        from django.core.files.storage import default_storage

        if self.picture:
            with contextlib.suppress(FileNotFoundError):
                default_storage.delete(self.picture_thumbnail.path)
            self.picture.delete()
        super().delete(*args, **kwargs)


class Competition(CreationModificationDateBase):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pilot = models.ForeignKey(
        to=Pilot,
        related_name="competitions",
        on_delete=models.CASCADE,
    )
    drone = models.ForeignKey(
        to=Drone,
        related_name="drone",
        on_delete=models.CASCADE,
    )
    distance_in_feet = models.IntegerField()
    distance_achievement_date = models.DateTimeField()

    class Meta:
        ordering = ("-distance_in_feet",)

    def __str__(self) -> str:
        return f"Competition by {self.pilot.name} with {self.drone.name}"
