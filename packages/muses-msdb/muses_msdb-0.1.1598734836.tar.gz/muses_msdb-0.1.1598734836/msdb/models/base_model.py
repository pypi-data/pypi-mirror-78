from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name=_('created at'),
        unique=False,
        null=False,
        blank=False,
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_('updated at'),
        unique=False,
        null=False,
        blank=False,
        auto_now=True
    )
    deleted_at = models.DateTimeField(
        verbose_name=_('deleted at'),
        unique=False,
        null=True,
        blank=True,
        db_index=True,
    )

    class Meta:
        abstract = True
