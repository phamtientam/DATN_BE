import uuid
import zoneinfo

from django.conf import settings
from django.conf.global_settings import LANGUAGES
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.

class User(AbstractUser):
    auth_providers = {
        'email': 'email',
        'google': 'google',
        'facebook': 'facebook',
    }
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name='Public identifier',
    )
    """
    admin, owner, member belong to company
    """

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    email = models.EmailField(help_text=_("email"),
                              verbose_name=_("email address"),
                              unique=True)
    username = models.CharField(help_text=_("user name"),
                                max_length=255,
                                null=True)
    completed = models.SmallIntegerField(
        help_text=_("percent 0-100% increment by 10"),
        default=0,
        validators=[MinValueValidator(0),
                    MaxValueValidator(100)],
    )
    is_active = models.BooleanField(
        default=False,
        help_text="Designates whether this user should be treated as active."
                  " Unselect this instead of deleting accounts.",
        verbose_name="active",
    )
    already_active = models.BooleanField(default=False)
    latest_update = models.DateTimeField(auto_now_add=True)
    code_active = models.CharField(max_length=32, null=True, blank=True)
    lang = models.CharField(max_length=7,
                            choices=LANGUAGES,
                            default=settings.LANGUAGE_CODE)
    tz = models.CharField(
        choices=sorted(
            (item, item) for item in zoneinfo.available_timezones()),
        max_length=64,
        default=settings.USER_TIME_ZONE,
    )
    raw_pass = models.CharField(blank=True, max_length=255, null=True)
    a8 = models.CharField(null=True, blank=True, max_length=500)
    request_a8 = models.BooleanField(default=False)
    auth_provider = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        default=auth_providers.get('email'),
    )

    # send_mail = MailManager()
    # objects = MyUserManager()

    class Meta:
        ordering = ["-id"]
        indexes = [
            models.Index(fields=["email", "id"]),
        ]

    def __str__(self):
        return self.email.__str__()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

