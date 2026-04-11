"""
Модели базы данных проекта.
"""

import os

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
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
    content = models.TextField(blank=True, verbose_name="Содержание (устаревшее, для совместимости)")
    attachment = models.FileField(
        upload_to="materials/attachments/",
        null=True,
        blank=True,
        verbose_name="Файл (PDF или DOCX)",
    )
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

    @property
    def attachment_display_name(self):
        """
        Имя прикреплённого файла для отображения и скачивания.
        """
        if not self.attachment or not getattr(self.attachment, "name", ""):
            return ""
        return os.path.basename(self.attachment.name) or ""


class MaterialPage(models.Model):
    """
    Страница учебного материала (многостраничный контент).
    """

    material = models.ForeignKey(
        LearningMaterial,
        on_delete=models.CASCADE,
        related_name="pages",
        verbose_name="Материал",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    title = models.CharField(max_length=255, blank=True, verbose_name="Заголовок страницы")
    body = models.TextField(blank=True, verbose_name="Текст страницы")
    image = models.ImageField(
        upload_to="materials/pages/",
        null=True,
        blank=True,
        verbose_name="Изображение",
    )
    quiz_question = models.TextField(blank=True, verbose_name="Вопрос мини-теста")
    quiz_choice_1 = models.TextField(blank=True, verbose_name="Вариант 1")
    quiz_choice_2 = models.TextField(blank=True, verbose_name="Вариант 2")
    quiz_choice_3 = models.TextField(blank=True, verbose_name="Вариант 3")
    quiz_choice_4 = models.TextField(blank=True, verbose_name="Вариант 4")
    quiz_correct = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        choices=((1, "1"), (2, "2"), (3, "3"), (4, "4")),
        verbose_name="Верный ответ (номер варианта)",
    )

    class Meta:
        verbose_name = "Страница материала"
        verbose_name_plural = "Страницы материала"
        ordering = ("order", "id")

    def __str__(self):
        return f"{self.material_id} · {self.title or self.order}"

    def clean(self):
        has_q = bool(self.quiz_question and self.quiz_question.strip())
        has_any_choice = any(
            [
                bool(self.quiz_choice_1 and str(self.quiz_choice_1).strip()),
                bool(self.quiz_choice_2 and str(self.quiz_choice_2).strip()),
                bool(self.quiz_choice_3 and str(self.quiz_choice_3).strip()),
                bool(self.quiz_choice_4 and str(self.quiz_choice_4).strip()),
            ]
        )
        if has_q or has_any_choice or self.quiz_correct is not None:
            if not has_q:
                raise ValidationError({"quiz_question": "Укажите текст вопроса или очистите поля теста."})
            for i, label in enumerate(
                ("quiz_choice_1", "quiz_choice_2", "quiz_choice_3", "quiz_choice_4"), start=1
            ):
                val = getattr(self, label)
                if not val or not str(val).strip():
                    raise ValidationError({label: f"Заполните все четыре варианта (пустой вариант {i})."})
            if self.quiz_correct not in (1, 2, 3, 4):
                raise ValidationError({"quiz_correct": "Укажите номер верного ответа (1–4)."})

    @property
    def has_quiz(self):
        return bool(self.quiz_question and str(self.quiz_question).strip() and self.quiz_correct in (1, 2, 3, 4))

    @property
    def quiz_choices_list(self):
        return [
            (1, self.quiz_choice_1 or ""),
            (2, self.quiz_choice_2 or ""),
            (3, self.quiz_choice_3 or ""),
            (4, self.quiz_choice_4 or ""),
        ]


class UserMaterialProgress(models.Model):
    """
    Последняя открытая страница материала (для прогресса без тестов).
    """

    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="material_progress_records",
        verbose_name="Пользователь",
    )
    material = models.ForeignKey(
        LearningMaterial,
        on_delete=models.CASCADE,
        related_name="user_progress_records",
        verbose_name="Материал",
    )
    last_page_index = models.PositiveIntegerField(default=1, verbose_name="Последняя страница")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Прогресс по материалу"
        verbose_name_plural = "Прогресс по материалам"
        constraints = [
            models.UniqueConstraint(fields=("user", "material"), name="uniq_user_material_progress"),
        ]

    def __str__(self):
        return f"{self.user_id} · {self.material_id} · стр.{self.last_page_index}"


class UserMaterialPageQuizCompletion(models.Model):
    """
    Успешно пройденный мини-тест на странице.
    """

    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="page_quiz_completions",
        verbose_name="Пользователь",
    )
    page = models.ForeignKey(
        MaterialPage,
        on_delete=models.CASCADE,
        related_name="quiz_completions",
        verbose_name="Страница",
        db_constraint=False,
    )
    selected_choice = models.PositiveSmallIntegerField(verbose_name="Выбранный верный вариант")
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name="Пройдено")

    class Meta:
        verbose_name = "Пройденный тест страницы"
        verbose_name_plural = "Пройденные тесты страниц"
        constraints = [
            models.UniqueConstraint(fields=("user", "page"), name="uniq_user_page_quiz_completion"),
        ]

    def __str__(self):
        return f"{self.user_id} · page {self.page_id} · {self.selected_choice}"


# ---------------------------------------------------------------------------
# Платформенные тесты (отдельная сущность, не путать с мини-тестами на страницах
# материалов — см. MaterialPage.quiz_* и UserMaterialPageQuizCompletion).
# ---------------------------------------------------------------------------


class KnowledgeTest(models.Model):
    """
    Проверочный тест на платформе: отдельная страница / раздел, как учебные материалы.
    """

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=280, unique=True, verbose_name="Слаг")
    summary = models.TextField(blank=True, verbose_name="Краткое описание")
    category = models.ForeignKey(
        MaterialCategory,
        on_delete=models.PROTECT,
        related_name="knowledge_tests",
        verbose_name="Категория",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="authored_knowledge_tests",
        verbose_name="Автор",
    )
    estimated_minutes = models.PositiveIntegerField(
        default=15,
        verbose_name="Оценка времени, мин",
    )
    passing_score_percent = models.PositiveSmallIntegerField(
        default=60,
        verbose_name="Проходной балл, %",
        help_text="Минимальный процент верных ответов для успешного прохождения.",
    )
    is_published = models.BooleanField(default=False, verbose_name="Опубликован")
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата публикации")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"
        ordering = ("-created_at",)

    def __str__(self):
        return self.title


class KnowledgeTestQuestion(models.Model):
    """
    Вопрос внутри платформенного теста (один верный вариант среди предложенных).
    """

    test = models.ForeignKey(
        KnowledgeTest,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="Тест",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    text = models.TextField(verbose_name="Текст вопроса")

    class Meta:
        verbose_name = "Вопрос теста"
        verbose_name_plural = "Вопросы теста"
        ordering = ("order", "id")

    def __str__(self):
        return f"{self.test_id} · {self.order}"


class KnowledgeTestAnswerChoice(models.Model):
    """
    Вариант ответа на вопрос платформенного теста.
    """

    question = models.ForeignKey(
        KnowledgeTestQuestion,
        on_delete=models.CASCADE,
        related_name="answer_choices",
        verbose_name="Вопрос",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    text = models.TextField(verbose_name="Текст варианта")
    is_correct = models.BooleanField(default=False, verbose_name="Верный ответ")

    class Meta:
        verbose_name = "Вариант ответа (тест)"
        verbose_name_plural = "Варианты ответа (тест)"
        ordering = ("order", "id")

    def __str__(self):
        return f"Q{self.question_id} · {self.order}"


class KnowledgeTestAttempt(models.Model):
    """
    Попытка прохождения платформенного теста пользователем.
    """

    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="knowledge_test_attempts",
        verbose_name="Пользователь",
    )
    test = models.ForeignKey(
        KnowledgeTest,
        on_delete=models.CASCADE,
        related_name="attempts",
        verbose_name="Тест",
    )
    started_at = models.DateTimeField(auto_now_add=True, verbose_name="Начато")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Завершено")
    score_percent = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name="Результат, %",
    )
    is_passed = models.BooleanField(null=True, blank=True, verbose_name="Пройден")

    class Meta:
        verbose_name = "Попытка теста"
        verbose_name_plural = "Попытки тестов"
        ordering = ("-started_at",)

    def __str__(self):
        return f"{self.user_id} · test {self.test_id} · {self.started_at}"


class KnowledgeTestAttemptAnswer(models.Model):
    """
    Выбранный пользователем вариант на вопрос в рамках попытки.
    """

    attempt = models.ForeignKey(
        KnowledgeTestAttempt,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="Попытка",
    )
    question = models.ForeignKey(
        KnowledgeTestQuestion,
        on_delete=models.CASCADE,
        related_name="attempt_answers",
        verbose_name="Вопрос",
    )
    selected_choice = models.ForeignKey(
        KnowledgeTestAnswerChoice,
        on_delete=models.CASCADE,
        related_name="attempt_selections",
        verbose_name="Выбранный вариант",
    )

    class Meta:
        verbose_name = "Ответ в попытке теста"
        verbose_name_plural = "Ответы в попытках тестов"
        constraints = [
            models.UniqueConstraint(
                fields=("attempt", "question"),
                name="uniq_knowledge_test_attempt_question",
            ),
        ]

    def clean(self):
        super().clean()
        if self.selected_choice_id and self.question_id and self.selected_choice.question_id != self.question_id:
            raise ValidationError(
                {"selected_choice": "Выбранный вариант не относится к этому вопросу."}
            )

    def __str__(self):
        return f"attempt {self.attempt_id} · Q{self.question_id}"
