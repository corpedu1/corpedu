"""
Представления проекта.
"""

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render

from .forms import LoginForm, ProfileForm, RegisterForm
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
