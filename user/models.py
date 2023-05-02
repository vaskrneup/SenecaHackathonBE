from django.apps import apps
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, government_id, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not government_id:
            raise ValueError("The given username must be set")

        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(  # NOQA
            self.model._meta.app_label,
            self.model._meta.object_name
        )
        government_id = GlobalUserModel.normalize_username(government_id)
        user = self.model(government_id=government_id, email=email, **extra_fields)

        user.password = make_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, government_id, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(government_id, email, password, **extra_fields)

    def create_superuser(self, government_id, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(government_id, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    government_id_validator = UnicodeUsernameValidator()

    first_name = models.CharField(
        verbose_name=_("First Name"),
        max_length=256,
    )
    last_name = models.CharField(
        verbose_name=_("Last Name"),
        max_length=256,
    )

    government_id = models.CharField(
        verbose_name=_("Government ID"),
        max_length=150,
        unique=True,
        help_text=_(
            "The government ID must contain at max 150 characters. Only Letters, digits and @/./+/-/_ are allowed."
        ),
        validators=[government_id_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        verbose_name=_("email address"),
        blank=False,
        null=False,
        unique=True,
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "government_id"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.government_id
