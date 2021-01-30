from django.db import models


class CreationModificationDateBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# TODO: create get_absolute_url model mixin
# TODO: create meta tags model mixin