"""
Представления проекта.
"""

import json

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Count, Max
from django.db.models.deletion import ProtectedError
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.text import slugify
from django.views.decorators.http import require_POST

from .forms import (
    CuratorKnowledgeTestForm,
    CuratorMaterialForm,
    KnowledgeTestQuestionEntryForm,
    LoginForm,
    MaterialPageFormSet,
    MaterialPageFormSetCreate,
    ProfileForm,
    RegisterForm,
)
from .models import (
    KnowledgeTest,
    KnowledgeTestAnswerChoice,
    KnowledgeTestQuestion,
    LearningMaterial,
    MaterialCategory,
    MaterialPage,
    User,
    UserMaterialPageQuizCompletion,
    UserMaterialProgress,
    UserRole,
)


def _compute_material_progress_percent(user, material):
    """
    Процент прохождения: по тестам, если они есть; иначе по последней странице.
    """
    pages = list(material.pages.all())
    total_pages = len(pages)
    quiz_pages = [p for p in pages if p.has_quiz]
    if quiz_pages:
        n = len(quiz_pages)
        passed = UserMaterialPageQuizCompletion.objects.filter(
            user=user, page_id__in=[p.id for p in quiz_pages]
        ).count()
        return round(100 * passed / n) if n else 0
    if total_pages == 0:
        return 0
    prog = UserMaterialProgress.objects.filter(user=user, material=material).first()
    last = prog.last_page_index if prog else 1
    last = min(max(last, 1), total_pages)
    return round(100 * last / total_pages)


def _is_administrator(user):
    """
    Проверяет, что пользователь является администратором.
    """
    return user.is_authenticated and user.role == UserRole.ADMINISTRATOR


def _is_curator(user):
    """
    Проверяет, что пользователь является куратором.
    """
    return user.is_authenticated and user.role == UserRole.CURATOR


def _build_unique_material_slug(title, current_id=None):
    """
    Формирует уникальный слаг для учебного материала.
    """
    base_slug = slugify(title) or "material"
    slug = base_slug
    index = 1
    queryset = LearningMaterial.objects.all()
    if current_id is not None:
        queryset = queryset.exclude(pk=current_id)
    while queryset.filter(slug=slug).exists():
        index += 1
        slug = f"{base_slug}-{index}"
    return slug


def _build_unique_knowledge_test_slug(title, current_id=None):
    """
    Формирует уникальный слаг для платформенного теста.
    """
    base_slug = slugify(title) or "test"
    slug = base_slug
    index = 1
    queryset = KnowledgeTest.objects.all()
    if current_id is not None:
        queryset = queryset.exclude(pk=current_id)
    while queryset.filter(slug=slug).exists():
        index += 1
        slug = f"{base_slug}-{index}"
    return slug


def _formset_has_non_deleted_page(formset):
    """
    True, если после is_valid() есть хотя бы одна страница без флага DELETE.
    """
    for f in formset.forms:
        cd = getattr(f, "cleaned_data", None)
        if not cd:
            continue
        if cd.get("DELETE"):
            continue
        return True
    return False


def _save_material_page_formset(formset):
    """
    Сохраняет страницы материала и выставляет порядок по порядку форм.
    """
    instances = formset.save(commit=False)
    for obj in formset.deleted_objects:
        obj.delete()
    for i, obj in enumerate(instances):
        obj.order = i
        obj.save()
    formset.save_m2m()


def _build_unique_category_slug(name, current_id=None):
    """
    Формирует уникальный слаг для категории.
    """
    base_slug = slugify(name) or "category"
    slug = base_slug
    index = 1
    queryset = MaterialCategory.objects.all()
    if current_id is not None:
        queryset = queryset.exclude(pk=current_id)
    while queryset.filter(slug=slug).exists():
        index += 1
        slug = f"{base_slug}-{index}"
    return slug


def landing(request):
    """
    Отображает главную страницу веб-сервиса.
    """
    return render(request, "landing.html")


def about(request):
    """
    Отображает страницу «О нас».
    """
    return render(request, "about.html")


def contacts(request):
    """
    Отображает страницу «Контакты».
    """
    return render(request, "contacts.html")


def feedback(request):
    """
    Отображает страницу «Обратная связь».
    """
    return render(request, "feedback.html")


def faq(request):
    """
    Отображает страницу «FAQ».
    """
    return render(request, "faq.html")


def materials(request):
    """
    Отображает страницу списка обучающих материалов.
    """
    items = LearningMaterial.objects.filter(is_published=True).select_related("category", "author")
    return render(request, "materials.html", {"materials": items})


def knowledge_tests(request):
    """
    Список опубликованных платформенных тестов.
    """
    items = (
        KnowledgeTest.objects.filter(is_published=True)
        .select_related("category", "author")
        .annotate(question_count=Count("questions"))
    )
    return render(request, "knowledge_tests.html", {"tests": items})


def knowledge_test_detail(request, slug):
    """
    Карточка теста (публично, только опубликованные).
    """
    test = get_object_or_404(
        KnowledgeTest.objects.filter(is_published=True)
        .select_related("category", "author")
        .annotate(question_count=Count("questions"))
        .prefetch_related("questions__answer_choices"),
        slug=slug,
    )
    return render(request, "knowledge_test_detail.html", {"test": test})


def material_detail(request, slug):
    """
    Отображает страницу детального просмотра обучающего материала.
    """
    material = get_object_or_404(
        LearningMaterial.objects.select_related("category", "author").prefetch_related("pages"),
        slug=slug,
    )
    can_view_draft = request.user.is_authenticated and (
        request.user.role == UserRole.ADMINISTRATOR
        or material.author_id == request.user.id
    )
    if not material.is_published and not can_view_draft:
        return redirect("materials")
    pages = list(material.pages.all())
    total_pages = len(pages)
    try:
        page_index = max(1, int(request.GET.get("page", 1)))
    except (TypeError, ValueError):
        page_index = 1
    if total_pages == 0:
        current_page = None
        page_index = 0
    else:
        if page_index > total_pages:
            page_index = total_pages
        current_page = pages[page_index - 1]
    prev_page = page_index - 1 if page_index > 1 else None
    next_page = page_index + 1 if total_pages and page_index < total_pages else None

    current_page_quiz_completion = None
    if request.user.is_authenticated and current_page and current_page.has_quiz:
        current_page_quiz_completion = UserMaterialPageQuizCompletion.objects.filter(
            user=request.user, page_id=current_page.pk
        ).first()

    if request.user.is_authenticated and total_pages > 0 and page_index >= 1:
        UserMaterialProgress.objects.update_or_create(
            user=request.user,
            material=material,
            defaults={"last_page_index": page_index},
        )

    progress_percent = None
    if request.user.is_authenticated:
        progress_percent = _compute_material_progress_percent(request.user, material)

    return render(
        request,
        "material_detail.html",
        {
            "material": material,
            "pages": pages,
            "current_page": current_page,
            "page_index": page_index,
            "total_pages": total_pages,
            "prev_page": prev_page,
            "next_page": next_page,
            "current_page_quiz_completion": current_page_quiz_completion,
            "progress_percent": progress_percent,
        },
    )


@login_required
@require_POST
def material_quiz_complete(request, slug):
    """
    Сохраняет успешное прохождение мини-теста (только верный ответ).
    """
    material = get_object_or_404(LearningMaterial.objects.prefetch_related("pages"), slug=slug)
    can_view_draft = request.user.role == UserRole.ADMINISTRATOR or material.author_id == request.user.id
    if not material.is_published and not can_view_draft:
        return HttpResponseBadRequest("forbidden")

    try:
        data = json.loads(request.body.decode())
    except (json.JSONDecodeError, UnicodeDecodeError, AttributeError):
        return HttpResponseBadRequest("json")

    page_id = data.get("page_id")
    choice = data.get("choice")
    try:
        page_id = int(page_id)
        choice = int(choice)
    except (TypeError, ValueError):
        return HttpResponseBadRequest("bad id")

    page = MaterialPage.objects.filter(pk=page_id, material_id=material.id).first()
    if page is None or not page.has_quiz:
        return HttpResponseBadRequest("page")
    if choice != page.quiz_correct:
        return JsonResponse({"ok": False, "error": "not_correct"}, status=400)

    UserMaterialPageQuizCompletion.objects.update_or_create(
        user=request.user,
        page=page,
        defaults={"selected_choice": choice},
    )
    pct = _compute_material_progress_percent(request.user, material)
    return JsonResponse({"ok": True, "progress_percent": pct})


def register(request):
    """
    Отображает и обрабатывает страницу «Регистрация».
    """
    if request.user.is_authenticated:
        return redirect("landing")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("landing")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login(request):
    """
    Отображает и обрабатывает страницу «Вход».
    """
    if request.user.is_authenticated:
        return redirect("landing")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            auth_login(request, form.cleaned_data["user"])
            return redirect("landing")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def logout(request):
    """
    Выполняет выход пользователя из системы.
    """
    if request.method == "POST":
        auth_logout(request)
    return redirect("landing")


@login_required
def settings(request):
    """
    Отображает и обрабатывает страницу «Настройки».
    """
    profile_form = ProfileForm(instance=request.user)
    password_form = PasswordChangeForm(user=request.user)
    if request.method == "POST":
        if "save_profile" in request.POST:
            profile_form = ProfileForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                return redirect("settings")
            password_form = PasswordChangeForm(user=request.user)
        if "save_password" in request.POST:
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                return redirect("settings")
            profile_form = ProfileForm(instance=request.user)
    return render(
        request,
        "settings.html",
        {
            "profile_form": profile_form,
            "password_form": password_form,
        },
    )


@login_required
def cabinet(request):
    """
    Личный кабинет: прогресс только по материалам, которые пользователь открывал
    (есть запись UserMaterialProgress; процент может быть 0%).
    """
    progress_records = (
        UserMaterialProgress.objects.filter(user=request.user, material__is_published=True)
        .select_related("material", "material__category")
        .prefetch_related("material__pages")
        .order_by("-updated_at")
    )
    material_progress_rows = [
        {
            "material": rec.material,
            "percent": _compute_material_progress_percent(request.user, rec.material),
        }
        for rec in progress_records
    ]
    return render(
        request,
        "cabinet.html",
        {"material_progress_rows": material_progress_rows},
    )


@login_required
def admin_panel(request):
    """
    Отображает кастомную панель администратора.
    """
    if not _is_administrator(request.user):
        return redirect("landing")
    context = {
        "users_count": User.objects.count(),
        "curators_count": User.objects.filter(role=UserRole.CURATOR).count(),
        "materials_count": LearningMaterial.objects.count(),
        "published_materials_count": LearningMaterial.objects.filter(is_published=True).count(),
        "categories_count": MaterialCategory.objects.count(),
    }
    return render(request, "admin_panel.html", context)


@login_required
def admin_user_roles(request):
    """
    Отображает и обрабатывает страницу изменения ролей пользователей.
    """
    if not _is_administrator(request.user):
        return redirect("landing")
    users = User.objects.order_by("username")
    allowed_roles = (
        UserRole.USER,
        UserRole.ADMINISTRATOR,
        UserRole.CURATOR,
    )
    role_choices = [choice for choice in UserRole.choices if choice[0] in allowed_roles]
    error_message = ""
    success_message = ""
    selected_user_id = ""
    selected_role = ""
    if request.method == "POST":
        selected_user_id = request.POST.get("user_id", "").strip()
        selected_role = request.POST.get("role", "").strip()
        if not selected_user_id or not selected_role:
            error_message = "Выберите пользователя и роль."
        elif selected_role not in allowed_roles:
            error_message = "Указана недопустимая роль."
        else:
            try:
                target_user = User.objects.get(pk=selected_user_id)
            except User.DoesNotExist:
                error_message = "Пользователь не найден."
            else:
                target_user.role = selected_role
                if selected_role == UserRole.ADMINISTRATOR:
                    target_user.is_staff = True
                target_user.save(update_fields=["role", "is_staff"])
                success_message = f"Роль пользователя {target_user.username} успешно обновлена."
                selected_user_id = str(target_user.pk)
    context = {
        "users": users,
        "role_choices": role_choices,
        "error_message": error_message,
        "success_message": success_message,
        "selected_user_id": selected_user_id,
        "selected_role": selected_role,
    }
    return render(request, "admin_user_roles.html", context)


@login_required
def admin_material_categories(request):
    """
    Отображает и обрабатывает страницу управления категориями материалов.
    """
    if not _is_administrator(request.user):
        return redirect("landing")
    error_message = ""
    success_message = ""
    if request.method == "POST":
        action = request.POST.get("action", "").strip()
        if action == "create":
            name = request.POST.get("name", "").strip()
            description = request.POST.get("description", "").strip()
            if not name:
                error_message = "Введите название категории."
            else:
                category = MaterialCategory(
                    name=name,
                    slug=_build_unique_category_slug(name),
                    description=description,
                )
                try:
                    category.full_clean()
                    category.save()
                    success_message = "Категория успешно создана."
                except ValidationError as error:
                    error_message = "; ".join(error.messages)
        elif action in {"update", "delete"}:
            category_id = request.POST.get("category_id", "").strip()
            try:
                category = MaterialCategory.objects.get(pk=category_id)
            except MaterialCategory.DoesNotExist:
                error_message = "Категория не найдена."
            else:
                if action == "delete":
                    try:
                        category.delete()
                        success_message = "Категория успешно удалена."
                    except ProtectedError:
                        error_message = "Нельзя удалить категорию, к которой привязаны материалы."
                else:
                    name = request.POST.get("name", "").strip()
                    description = request.POST.get("description", "").strip()
                    if not name:
                        error_message = "Название категории не может быть пустым."
                    else:
                        category.name = name
                        category.slug = _build_unique_category_slug(name, current_id=category.id)
                        category.description = description
                        try:
                            category.full_clean()
                            category.save()
                            success_message = "Категория успешно обновлена."
                        except ValidationError as error:
                            error_message = "; ".join(error.messages)
    categories = MaterialCategory.objects.order_by("name")
    return render(
        request,
        "admin_material_categories.html",
        {
            "categories": categories,
            "error_message": error_message,
            "success_message": success_message,
        },
    )


@login_required
def curator_panel(request):
    """
    Отображает панель управления куратора.
    """
    if not _is_curator(request.user):
        return redirect("landing")
    context = {
        "materials_count": LearningMaterial.objects.filter(author=request.user).count(),
        "published_materials_count": LearningMaterial.objects.filter(author=request.user, is_published=True).count(),
        "draft_materials_count": LearningMaterial.objects.filter(author=request.user, is_published=False).count(),
        "tests_count": KnowledgeTest.objects.filter(author=request.user).count(),
        "published_tests_count": KnowledgeTest.objects.filter(author=request.user, is_published=True).count(),
        "draft_tests_count": KnowledgeTest.objects.filter(author=request.user, is_published=False).count(),
    }
    return render(request, "curator_panel.html", context)


@login_required
def curator_material_create(request):
    """
    Отображает и обрабатывает страницу создания учебного материала.
    """
    if not _is_curator(request.user):
        return redirect("landing")
    success_message = ""
    error_message = ""
    if request.method == "POST":
        form = CuratorMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.author = request.user
            material.slug = _build_unique_material_slug(material.title)
            if material.is_published:
                material.published_at = timezone.now()
            else:
                material.published_at = None
            material.content = ""
            material.save()
            page_formset = MaterialPageFormSetCreate(request.POST, request.FILES, instance=material)
            if page_formset.is_valid() and _formset_has_non_deleted_page(page_formset):
                _save_material_page_formset(page_formset)
                success_message = "Учебный материал успешно создан."
                form = CuratorMaterialForm()
                page_formset = MaterialPageFormSetCreate(instance=LearningMaterial())
            else:
                material.delete()
                if page_formset.is_valid() and not _formset_has_non_deleted_page(page_formset):
                    error_message = "Добавьте хотя бы одну страницу материала."
                else:
                    error_message = "Исправьте ошибки в блоках страниц."
                form = CuratorMaterialForm(request.POST, request.FILES)
                page_formset = MaterialPageFormSetCreate(request.POST, request.FILES)
        else:
            page_formset = MaterialPageFormSetCreate(request.POST, request.FILES)
    else:
        form = CuratorMaterialForm()
        page_formset = MaterialPageFormSetCreate(instance=LearningMaterial())
    return render(
        request,
        "curator_material_create.html",
        {
            "form": form,
            "page_formset": page_formset,
            "success_message": success_message,
            "error_message": error_message,
        },
    )


@login_required
def curator_materials_manage(request):
    """
    Отображает страницу списка материалов куратора.
    """
    if not _is_curator(request.user):
        return redirect("landing")
    items = LearningMaterial.objects.filter(author=request.user).select_related("category").order_by("-created_at")
    return render(request, "curator_materials_manage.html", {"materials": items})


@login_required
def curator_material_edit(request, slug):
    """
    Отображает и обрабатывает страницу детального редактирования материала куратора.
    """
    if not _is_curator(request.user):
        return redirect("landing")
    material = get_object_or_404(
        LearningMaterial.objects.prefetch_related("pages"),
        slug=slug,
        author=request.user,
    )
    success_message = ""
    error_message = ""
    form = CuratorMaterialForm(instance=material)
    page_formset = MaterialPageFormSet(instance=material)
    if request.method == "POST":
        action = request.POST.get("action", "").strip()
        if action == "delete":
            material.delete()
            return redirect("curator_materials_manage")
        if action == "remove_attachment":
            material.attachment = None
            material.save(update_fields=["attachment"])
            success_message = "Файл удален."
            form = CuratorMaterialForm(instance=material)
            page_formset = MaterialPageFormSet(instance=material)
        else:
            form = CuratorMaterialForm(request.POST, request.FILES, instance=material)
            page_formset = MaterialPageFormSet(request.POST, request.FILES, instance=material)
            if form.is_valid() and page_formset.is_valid():
                updated = form.save(commit=False)
                updated.author = request.user
                updated.slug = _build_unique_material_slug(updated.title, current_id=updated.id)
                if updated.is_published and updated.published_at is None:
                    updated.published_at = timezone.now()
                if not updated.is_published:
                    updated.published_at = None
                updated.save()
                _save_material_page_formset(page_formset)
                success_message = "Материал обновлен."
                material = updated
                form = CuratorMaterialForm(instance=material)
                page_formset = MaterialPageFormSet(instance=material)
            else:
                error_message = "Проверьте корректность заполнения формы и страниц."
    return render(
        request,
        "curator_material_edit.html",
        {
            "form": form,
            "page_formset": page_formset,
            "material": material,
            "error_message": error_message,
            "success_message": success_message,
        },
    )


@login_required
def curator_knowledge_tests_manage(request):
    """
    Список платформенных тестов куратора.
    """
    if not _is_curator(request.user):
        return redirect("landing")
    items = KnowledgeTest.objects.filter(author=request.user).select_related("category").order_by("-created_at")
    return render(request, "curator_knowledge_tests_manage.html", {"tests": items})


@login_required
@require_POST
def curator_knowledge_test_set_publish(request, slug):
    """
    Публикация или снятие теста с публикации (только автор-куратор).
    """
    if not _is_curator(request.user):
        return redirect("landing")
    test = get_object_or_404(KnowledgeTest, slug=slug, author=request.user)
    publish = request.POST.get("publish")
    if publish == "1":
        test.is_published = True
        if test.published_at is None:
            test.published_at = timezone.now()
    elif publish == "0":
        test.is_published = False
        test.published_at = None
    else:
        return redirect("curator_knowledge_tests_manage")
    test.save(update_fields=["is_published", "published_at", "updated_at"])
    next_page = request.POST.get("next_page", "manage")
    if next_page == "edit":
        return redirect("curator_knowledge_test_edit", slug=test.slug)
    return redirect("curator_knowledge_tests_manage")


@login_required
def curator_knowledge_test_create(request):
    """
    Создание платформенного теста: после сохранения — переход к редактированию вопросов.
    """
    if not _is_curator(request.user):
        return redirect("landing")
    error_message = ""
    if request.method == "POST":
        form = CuratorKnowledgeTestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.author = request.user
            test.slug = _build_unique_knowledge_test_slug(test.title)
            if test.is_published:
                test.published_at = timezone.now()
            else:
                test.published_at = None
            test.save()
            return redirect("curator_knowledge_test_edit", slug=test.slug)
        error_message = "Проверьте корректность заполнения полей."
    else:
        form = CuratorKnowledgeTestForm()
    return render(
        request,
        "curator_knowledge_test_create.html",
        {"form": form, "error_message": error_message},
    )


@login_required
def curator_knowledge_test_edit(request, slug):
    """
    Редактирование теста и добавление вопросов с вариантами ответов.
    """
    if not _is_curator(request.user):
        return redirect("landing")
    test = get_object_or_404(KnowledgeTest, slug=slug, author=request.user)
    success_message = ""
    error_message = ""
    test_form = CuratorKnowledgeTestForm(instance=test)
    question_form = KnowledgeTestQuestionEntryForm()

    if request.method == "POST":
        action = request.POST.get("action", "").strip()
        if action == "delete":
            test.delete()
            return redirect("curator_knowledge_tests_manage")
        if action == "delete_question":
            qid = request.POST.get("question_id")
            try:
                qid = int(qid)
            except (TypeError, ValueError):
                qid = None
            if qid:
                KnowledgeTestQuestion.objects.filter(pk=qid, test_id=test.id).delete()
                success_message = "Вопрос удалён."
        elif action == "add_question":
            question_form = KnowledgeTestQuestionEntryForm(request.POST)
            if question_form.is_valid():
                with transaction.atomic():
                    max_order = KnowledgeTestQuestion.objects.filter(test_id=test.id).aggregate(m=Max("order"))["m"] or 0
                    q = KnowledgeTestQuestion.objects.create(
                        test_id=test.id,
                        order=max_order + 1,
                        text=question_form.cleaned_data["text"].strip(),
                    )
                    cc = question_form.cleaned_data["correct_choice"]
                    for i in range(1, 5):
                        KnowledgeTestAnswerChoice.objects.create(
                            question=q,
                            order=i,
                            text=question_form.cleaned_data[f"choice_{i}"],
                            is_correct=(i == cc),
                        )
                success_message = "Вопрос добавлен."
                question_form = KnowledgeTestQuestionEntryForm()
            else:
                error_message = "Проверьте поля нового вопроса."
        else:
            test_form = CuratorKnowledgeTestForm(request.POST, instance=test)
            if test_form.is_valid():
                updated = test_form.save(commit=False)
                updated.author = request.user
                updated.slug = _build_unique_knowledge_test_slug(updated.title, current_id=updated.id)
                # Публикация только через кнопку на странице / списке, не через эту форму
                updated.is_published = test.is_published
                updated.published_at = test.published_at
                updated.save()
                test = updated
                success_message = "Данные теста сохранены."
                test_form = CuratorKnowledgeTestForm(instance=test)
            else:
                error_message = "Проверьте основные поля теста."

    questions = (
        KnowledgeTestQuestion.objects.filter(test_id=test.id)
        .prefetch_related("answer_choices")
        .order_by("order", "id")
    )
    return render(
        request,
        "curator_knowledge_test_edit.html",
        {
            "test": test,
            "test_form": test_form,
            "question_form": question_form,
            "questions": questions,
            "error_message": error_message,
            "success_message": success_message,
        },
    )
