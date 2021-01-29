import os

from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now as timezone_now

from rest_framework_simplejwt.tokens import RefreshToken


def upload_to(instance, filename):
    now = timezone_now()
    base, extention = os.path.splitext(filename)
    extention = extention.lower()

    return f"avatars/{now:%Y/%m/%d}/{instance.pk}{extention}"


class CustomUserManager(BaseUserManager):
    """
    Custom user manager
    """

    def create_superuser(self, email, username, password, **other_fields):
        """
        Create, save and return a new superuser
        """
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")

        return self.create_user(
            email=email, username=username, password=password, **other_fields
        )

    def create_user(self, email, username, password=None, **other_fields):
        """
        Create and return a normal new user
        """
        if not email:
            raise ValueError("User must have an email address.")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)

        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Database model for users in the system
    """

    email = models.EmailField(_("Email"), max_length=255, unique=True, db_index=True)
    username = models.CharField(_("Username"), max_length=255, unique=True)
    first_name = models.CharField(
        _("First Name"), max_length=255, null=True, blank=True
    )
    last_name = models.CharField(_("Last Name"), max_length=255, null=True, blank=True)
    bio = models.TextField(_("Bio"), max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(_("Avatar"), upload_to=upload_to, default="user.png")
    avatar_thumbnail = ImageSpecField(
        source="avatar",
        processors=[ResizeToFill(728, 250)],
        format="PNG",
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)

    def get_full_name(self) -> str:
        """Retrieve fullname of user"""
        return self.first_name

    def get_short_name(self) -> str:
        """Retrieve short name of user"""
        return self.last_name

    def __str__(self) -> str:
        return self.email

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}
