from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

# create custom super user
class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email=None, user_name=None, first_name=None, password=None, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")

        return self.create_user(email, user_name, first_name, password, **other_fields)

    def create_user(self, email=None, username=None, first_name=None, password=None, **other_fields):
        if not email:
            raise ValueError(gettext_lazy("You must provide an email address"))
        if not username:
            email = self.normalize_email(email)
            print(other_fields, email, username, first_name, password)

        email = self.normalize_email(email)
        user = self.model(
            email=email, user_name=username, first_name=first_name, **other_fields
        )
        user.set_password(password)
        user.save()
        return user


# create normal user
class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(gettext_lazy("email address"), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(gettext_lazy("about"), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    # modify default field to email
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["user_name", "first_name"]

    def __str__(self):
        return self.user_name
