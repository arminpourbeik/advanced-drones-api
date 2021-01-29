from django.contrib import admin

from apps.authentication.models import CustomUser

admin.site.register(CustomUser)
