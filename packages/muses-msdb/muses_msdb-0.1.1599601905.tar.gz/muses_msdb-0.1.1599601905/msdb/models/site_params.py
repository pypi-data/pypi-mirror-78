from django.db import models
from django.utils.translation import gettext_lazy as _

from . import BaseModel


class SiteParamManager(models.Manager):
    pass


class SiteParam(BaseModel):
    key = models.CharField(
        verbose_name=_('key'),
        unique=True,
        null=False,
        blank=False,
        db_index=True,
        max_length=255,
        default=_("no name")
    )
    value = models.CharField(
        verbose_name=_("value"),
        unique=True,
        null=False,
        blank=False,
        default=_('no value'),
        db_index=True,
        max_length=2048
    )

    objects = SiteParamManager()

    class Meta:
        verbose_name = 'site parameter'
        verbose_name_plural = 'site parameters'
