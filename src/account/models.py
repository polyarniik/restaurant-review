from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import (
    PermissionsMixin,
    UserManager as DjangoUserManager,
)
from django.db import models
from djchoices import DjangoChoices, ChoiceItem


class UserManager(DjangoUserManager):
    def create_user(self, email, password=None, **kwargs):
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.model(email=email, is_superuser=True)
        user.set_password(password)
        user.save()
        return user


class Role(DjangoChoices):
    admin = ChoiceItem(label="Администратор")
    user = ChoiceItem(label="Пользователь")


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(
        choices=Role.choices,
        default=Role.user,
        max_length=20,
        verbose_name="Роль",
    )

    def __str__(self):
        return f"{self.email}"

    @property
    def is_staff(self):
        return self.is_superuser

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
