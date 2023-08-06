import pytz
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from . import BaseModel


class MemberQuerySet(models.QuerySet):
    def superusers(self):
        return self.filter(is_superuser=True)

    def staff(self):
        return self.filter(is_staff=True)

    def privileges(self):
        return self.filter(status=Member.PRIVILEGE)

    def regulars(self):
        return self.filter(status=Member.REGULAR)


class MemberManager(BaseUserManager):
    def get_queryset(self):
        return MemberQuerySet(self.model, using=self._db)

    def superusers(self):
        return self.get_queryset().superusers()

    def staff(self):
        return self.get_queryset().staff()

    def privileges(self):
        return self.get_queryset().privileges()

    def regulars(self):
        return self.get_queryset().regulars()

    def create_user(self, username, email, date_of_birth, password=None, **kwargs):
        email = MemberManager.normalize_email(email)
        if password is None:
            password = MemberManager.make_random_password(self)
        member = Member(username=username, email=email, date_of_birth=date_of_birth)
        member.set_password(password)
        for key, value in kwargs.items():
            setattr(member, key, value)
        member.clean()
        member.save()

    def create_superuser(self, username, email, date_of_birth, password=None, **kwargs):
        if password is None:
            password = MemberManager.make_random_password(self)
        member = Member(username=username, email=email, date_of_birth=date_of_birth)
        member.is_staff = True
        member.is_superuser = True
        member.set_password(password)
        for key, value in kwargs.items():
            setattr(member, key, value)
        member.clean()
        member.save()


class Member(AbstractBaseUser, PermissionsMixin, BaseModel):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    date_of_birth = models.DateField()
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    def member_avatar_path(self, filename):
        return 'avatars/member_{0}/{1}'.format(self.id, filename)

    avatar = models.ImageField(
        verbose_name=_('avatar'),
        upload_to=member_avatar_path,
        storage=FileSystemStorage
    )
    web_site = models.URLField(
        verbose_name=_('web site'),
        max_length=2048,
    )
    gender = models.CharField(
        verbose_name=_('gender'),
        max_length=1
    )
    occupation = models.CharField(
        verbose_name=_('occupation'),
        max_length=255
    )
    phone_number = PhoneNumberField(
        verbose_name=_('phone number'),
        blank=True
    )
    privilege_start_date = models.DateField(
        verbose_name=_('privilege start date'),
        null=True
    )
    postal_address = models.CharField(
        verbose_name=_('postal address'),
        max_length=1024
    )
    postal_address_2 = models.CharField(
        verbose_name=_('postal address 2'),
        max_length=1024
    )
    postal_city = models.CharField(
        verbose_name=_('postal city'),
        max_length=200
    )
    postal_code = models.CharField(
        verbose_name=_('postal code'),
        max_length=20
    )
    language = models.CharField(
        verbose_name=_('language'),
        max_length=2
    )
    locked = models.BooleanField(
        verbose_name=_('locked'),
        default=False
    )

    """
    ------------------------------
    *** DEBUT LISTE DES THEMES ***
    ------------------------------
    Section à compléter pour ajouter des thèmes complémentaires
    """

    THEME_DEFAULT = "muses_default"
    THEME_CLASSIC = "muses_classic"
    THEME_ROSE = "muses_rose"
    THEME_BLUE = "muses_blue"
    THEME_GREEN = "muses_green"
    THEME_ORANGE = "muses_orange"

    THEME_CHOICES = (
        (THEME_DEFAULT, _("Default")),
        (THEME_CLASSIC, _("Classic")),
        (THEME_ROSE, _("Rose")),
        (THEME_BLUE, _("Blue")),
        (THEME_GREEN, _("Green")),
        (THEME_ORANGE, _("Orange")),
    )

    """
    ------------------------------
    *** FIN LISTE DES THEMES ***
    ------------------------------
    """

    theme = models.CharField(
        verbose_name=_('theme'),
        max_length=30,
        choices=THEME_CHOICES,
        default=THEME_DEFAULT
    )

    connections_counter = models.IntegerField(
        verbose_name=_('connections counter'),
        default=0,
    )
    page_views_counter = models.IntegerField(
        verbose_name=_('page views counter'),
        default=0,
    )

    email_notification_on_new_comment = models.BooleanField(
        verbose_name=_('email notification on new comment'),
        default=False
    )
    email_notification_on_new_message = models.BooleanField(
        verbose_name=_('email notification on new message'),
        default=False
    )

    mailbox_collapsing = models.BooleanField(
        verbose_name=_('mailbox collapsing'),
        default=False
    )
    mailbox_blocked = models.BooleanField(
        verbose_name=_('mailbox blocked'),
        default=False
    )

    ALL_TIMEZONES = sorted((item, item) for item in pytz.all_timezones)
    tz_name = models.CharField(choices=ALL_TIMEZONES, max_length=64)

    story = models.TextField(
        verbose_name=_('story'),
        default="",
        unique=False,
        blank=False,
        null=False
    )

    REGULAR = 'R'
    PRIVILEGE = 'P'
    MEMBER_STATUS_CHOICES = [
        (REGULAR, 'REGULAR'),
        (PRIVILEGE, 'PRIVILEGE')
    ]
    status = models.CharField(
        verbose_name=_('status'),
        max_length=10,
        choices=MEMBER_STATUS_CHOICES,
        default=REGULAR
    )

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth', 'email']

    blocked_contacts = models.ManyToManyField(
        to='self',
        related_name='blocked_contact'
    )

    objects = MemberManager()

    class Meta:
        verbose_name = _('member')
        verbose_name_plural = _('members')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
