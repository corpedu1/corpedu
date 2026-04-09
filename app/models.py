"""
Модели базы данных проекта.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    """
    Роли пользователей платформы.
    """

    USER = "user", "User"
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
        default=UserRole.USER,
        verbose_name="Роль",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def save(self, *args, **kwargs):
        """
        Устанавливает роль администратора для суперпользователя.
        """
        if self.is_superuser:
            self.role = UserRole.ADMINISTRATOR
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Возвращает отображаемое имя пользователя.
        """
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.username


class MaterialFormat(models.TextChoices):
    """
    Форматы обучающих материалов.
    """

    ARTICLE = "article", "Статья"
    GUIDE = "guide", "Инструкция"
    CHECKLIST = "checklist", "Чек-лист"
    VIDEO = "video", "Видео"
    PRESENTATION = "presentation", "Презентация"


class MaterialCategory(models.Model):
    """
    Категория обучающих материалов.
    """

    name = models.CharField(max_length=120, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=140, unique=True, verbose_name="Слаг")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Категория материала"
        verbose_name_plural = "Категории материалов"
        ordering = ("name",)

    def __str__(self):
        """
        Возвращает название категории.
        """
        return self.name


class LearningMaterial(models.Model):
    """
    Обучающий материал по информационной безопасности.
    """

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=280, unique=True, verbose_name="Слаг")
    summary = models.TextField(blank=True, verbose_name="Краткое описание")
    content = models.TextField(verbose_name="Содержание")
    material_format = models.CharField(
        max_length=20,
        choices=MaterialFormat.choices,
        default=MaterialFormat.ARTICLE,
        verbose_name="Формат",
    )
    category = models.ForeignKey(
        MaterialCategory,
        on_delete=models.PROTECT,
        related_name="materials",
        verbose_name="Категория",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="created_materials",
        verbose_name="Автор",
    )
    estimated_minutes = models.PositiveIntegerField(default=10, verbose_name="Оценка времени, мин")
    is_published = models.BooleanField(default=False, verbose_name="Опубликован")
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата публикации")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Обучающий материал"
        verbose_name_plural = "Обучающие материалы"
        ordering = ("-created_at",)

    def __str__(self):
        """
        Возвращает заголовок материала.
        """
        return self.title
