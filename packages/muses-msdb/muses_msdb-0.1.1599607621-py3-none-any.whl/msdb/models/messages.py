from django.db import models
from django.utils.translation import gettext_lazy as _

from . import BaseModel, Member


class MessageManager(models.Manager):
    pass


class Message(BaseModel):
    subject = models.CharField(
        verbose_name=_('subject'),
        unique=True,
        null=False,
        blank=False,
        db_index=True,
        max_length=255,
        default=_("no subject")
    )
    content = models.TextField(
        verbose_name=_('content'),
        unique=False,
        null=True,
        blank=True,
    )
    sender = models.ForeignKey(
        to=Member,
        related_name='sender_ref',
        on_delete=models.CASCADE
    )
    recipient = models.ManyToManyField(
        to=Member,
        verbose_name=_('recipient'),
        related_name='recipients',
        related_query_name='recipients'
    )
    message_box = models.ForeignKey(
        to=Member,
        related_name=_('message_box'),
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'

    def send(self):
        pass