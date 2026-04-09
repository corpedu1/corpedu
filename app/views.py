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
from .models import LearningMaterial


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
