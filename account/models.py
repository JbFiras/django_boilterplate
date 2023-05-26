from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from util.models import TimestampMixin
from django.utils.translation import gettext as _
from account.utils.managers import UserManager
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.

USER_TYPE_ADMIN = settings.USER_TYPE_ADMIN
USER_TYPE_CLIENT = settings.USER_TYPE_CLIENT
USER_TYPE_CRAFTMAN = settings.USER_TYPE_CRAFTMAN

USER_TYPES = [
    (USER_TYPE_ADMIN, _("Admin")),
    (USER_TYPE_CLIENT, _("Client")),
     (USER_TYPE_CRAFTMAN, _("Craftman")),
]

class User(AbstractBaseUser, PermissionsMixin, TimestampMixin):
    """Custom User class"""
    class Meta:
        verbose_name_plural = _("Users")
        verbose_name = _("User")
        ordering = ["email", "first_name", "last_name"]

    objects = UserManager()
    USERNAME_FIELD = "email"

    first_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("First name"),
    )
    last_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Last name"),
    )
    email = models.EmailField(max_length=255, unique=True, verbose_name=_("Email"))
    phone_number = models.CharField(
        max_length=255,
        default=None,
        blank=True,
        null=True,
        verbose_name=_("Phone number"),
    )
    type = models.CharField(
        max_length=255,
        default=USER_TYPE_ADMIN,
        choices=USER_TYPES,
        verbose_name=_("User type"),
        help_text=_("Designates the type of permission user will have."),
    )
    photo = models.ImageField(
        verbose_name=_("Photo"),
        upload_to="static/users_photos/",
        null=True,
        default=None,
        blank=True,
    )
    is_active = models.BooleanField(
        _("Active"),
        default=True,
    )
    is_superuser = models.BooleanField(
        _("Super User"),
        default=False,
    )

    def is_staff(self):
        return self.is_superuser

    def __str__(self):
        return f"{self.email}"

    @property
    def fullname(self):
        return " ".join([n for n in [self.first_name, self.last_name] if n]) if self.last_name else self.first_name

    @property
    def is_admin(self):
        return True if self.type == "admin" else False

    @property
    def photo_url(self):
        if self.photo:
            return self.photo.url
        return None

    # generate jwt token
    def get_jwt_token_for_user(self):
        """get jwt token for the user"""
        refresh = RefreshToken.for_user(self)
        access_token = refresh.access_token
        access_token["created_at"] = str(timezone.now())
        return {
            "access_token": str(access_token),
            "refresh_token": str(refresh),
        }
