from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.get_full_name()


class Balance(models.Model):
    """Модель баланса пользователя."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='balance',
        verbose_name='Пользователь',
        blank=True,
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1000.00,
        verbose_name='Баланс',
    )

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)

    def __str__(self):
        return f'{self.user.email}: {self.balance} бонусов' if self.user else 'Без пользователя'

    def save(self, *args, **kwargs):
        if self.balance < 0:
            self.balance = 0
        super().save(*args, **kwargs)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_balance(sender, instance, created, **kwargs):
    if created:
        Balance.objects.create(user=instance)


class Subscription(models.Model):
    """Модель подписки пользователя на курс."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Пользователь',
    )
    course = models.ForeignKey(
        'courses.Course',
        related_name='subscriptions',
        on_delete=models.CASCADE,
        verbose_name='Курс',
        blank=True,
    )
    access_granted = models.BooleanField(
        default=False,
        verbose_name='Доступ открыт',
    )
    subscription_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата подписки',
        blank=True,
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)

    def __str__(self):
        return f'Подписка {self.user.email} на {self.course.title}'
