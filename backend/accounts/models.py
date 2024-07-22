from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    ''' Модель пользователя. '''
    username_validator = RegexValidator(
        regex=r'^[\w.@+-]+$',
        message=(
            'Пользователь может использовать только буквы, '
            'цифры и @/./+/-/_ символы.'
        )
    )
    email = models.EmailField(
        max_length=50,
        unique=True,
        verbose_name='Почта'
    )
    username = models.CharField(
        blank=False,
        max_length=50,
        unique=True,
        verbose_name='Имя пользователя',
        validators=[username_validator]
    )
    first_name = models.CharField(
        blank=False,
        max_length=50,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        blank=False,
        max_length=50,
        verbose_name='Фамилия'
    )
    avatar = models.ImageField(
        upload_to='',
        blank=True,
        null=True
    )
    USERNAME_FIELD = 'email'
    # Логин в админку через e-mail.
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    # Суперпользователь создается с ФИО.

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Follow(models.Model):
    ''' Модель подписки. '''
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower',
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following',
    )

    class Meta:
        ordering = ('user', 'following',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
