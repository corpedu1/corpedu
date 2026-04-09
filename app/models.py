"""
Модели базы данных проекта.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    """
    Роли пользователей платформы.
    """

    ADMINISTRATOR = "administrator", "Администратор"
    CURATOR = "curator", "Куратор"
    EMPLOYEE = "employee", "Сотрудник"


class User(AbstractUser):
    """
    Кастомная модель пользователя системы.
    """

    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.EMPLOYEE,
        verbose_name="Роль",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        """
        Возвращает отображаемое имя пользователя.
        """
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.username
