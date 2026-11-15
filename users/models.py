from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Электронная почта", help_text="Введите электронную почту")
    phone_number = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Номер телефона", help_text="Введите номер телефона"
    )
    token = models.CharField(blank=True, null=True)
    username = models.CharField(unique=False, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("password1",)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["first_name", "last_name"]
        permissions = (("management", "Can manage users"),)
