import os

from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager as DjangoBaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class BaseUserManager(DjangoBaseUserManager):
    """
    Define a model manager for User model with no username field.
    """
    use_in_migrations = True

    def _create_user(self, email, password, birth_date, gender, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, birth_date, gender, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, birth_date, gender, **extra_fields)

    def create_superuser(self, email, password, birth_date, gender, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, birth_date, gender, **extra_fields)


class CustomUserModel(AbstractUser):
    """User model."""

    username = None

    email = models.EmailField(_("email address"), unique=True, help_text=_("Required. Your email address."))

    uuid = models.UUIDField(default=uuid.uuid4)

    birth_date = models.DateField(default=timezone.now, help_text=_("Required. Your birth date."))

    CHOICES = (('M', 'Male'), ('F', 'Female'))
    gender = models.CharField(max_length=1, choices=CHOICES, default='M', help_text=_("Required. Choose your gender."))

    phone_number = models.CharField(max_length=13, blank=True, null=True, help_text=_('Enter phone number'
                                                                                      ' e.g: +998123456789'))

    objects = BaseUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['birth_date', 'gender']

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        db_table = 'user'
        verbose_name = "user"
        verbose_name_plural = "users"


class CodeCheck(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)

