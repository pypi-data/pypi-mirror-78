from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext_lazy as _

from . import BaseModel


class SectionManager(models.Manager):
    pass


class Section(BaseModel):
    ACTIVE = 1
    DISABLED = 2
    STATUS_CHOICES = (
        (ACTIVE, _('active')),
        (DISABLED, _('disabled'))
    )
    short_name = models.CharField(
        verbose_name=_('short name'),
        unique=True,
        max_length=20,
        default=_('no short name'),
        db_index=True
    )
    name = models.CharField(
        verbose_name=_('name'),
        unique=False,
        max_length=255,
        default=_('no name'),
        db_index=True
    )
    order = models.IntegerField(
        verbose_name=_('order'),
        unique=True,
        default=0
    )
    description = models.TextField(
        verbose_name=_('description'),
        max_length=1024,
        null=True
    )
    status = models.IntegerField(
        verbose_name=_('status'),
        choices=STATUS_CHOICES,
        default=DISABLED
    )
    groups = models.ManyToManyField(
        to=Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this section belongs to.'
        ),
        related_name="section_set",
        related_query_name="section",
    )

    class Meta:
        verbose_name = _('section')
        verbose_name_plural = _('sections')
