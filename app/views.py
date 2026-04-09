"""
Представления проекта.
"""

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.text import slugify

from .forms import CuratorMaterialForm, LoginForm, ProfileForm, RegisterForm
from .models import LearningMaterial, MaterialCategory, User, UserRole


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


def _build_unique_material_slug(title):
    """
    Формирует уникальный слаг для учебного материала.
    """
    base_slug = slugify(title) or "material"
    slug = base_slug
    index = 1
    while LearningMaterial.objects.filter(slug=slug).exists():
        index += 1
        slug = f"{base_slug}-{index}"
    return slug


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


def material_detail(request, slug):
    """
    Отображает страницу детального просмотра обучающего материала.
    """
    material = get_object_or_404(
        LearningMaterial.objects.select_related("category", "author"),
        slug=slug,
    )
    can_view_draft = request.user.is_authenticated and (
        request.user.role == UserRole.ADMINISTRATOR
        or material.author_id == request.user.id
    )
    if not material.is_published and not can_view_draft:
        return redirect("materials")
    return render(request, "material_detail.html", {"material": material})


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
        {"profile_form": profile_form, "password_form": password_form},
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
            material.save()
            success_message = "Учебный материал успешно создан."
            form = CuratorMaterialForm()
    else:
        form = CuratorMaterialForm()
    return render(
        request,
        "curator_material_create.html",
        {"form": form, "success_message": success_message},
    )
