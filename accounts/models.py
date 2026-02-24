from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db import models
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    photo = models.ImageField(
        _("Фото профиля"),
        upload_to = "users/photos/",
        blank=True,
        null=True,
    )

    email = models.EmailField(
        'Email',
        unique=True
    )

    first_name = models.CharField(
        'Имя', 
        max_length=150,
        blank=True
    )

    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )

    # Новые поля
    patronymic = models.CharField(
        'Отчество',
        max_length=150,
        blank=True
    )

    birth_date = models.DateTimeField(
        'Дата рождения',
        blank=True,
        null=True
    )

    GENDER_CHOICES = [
        ("male", "Мужской"),
        ("female", "женский"),
    ]

    gender = models.CharField(
        'Пол',
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True
    )

    citizenship = models.CharField(
        'Гражданство',
        max_length=150,
        blank=True
    )

    is_staff = models.BooleanField(
        default=False
        )

    is_active = models.BooleanField(
        default=True
        )

    date_joined = models.DateTimeField(
        auto_now_add=True
        )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name'] # Добавил что ты написал


    class Meta:
        verbose_name = 'Личные данные'
        verbose_name_plural = 'Личные данные'

    def __str__(self):
        return self.email   

