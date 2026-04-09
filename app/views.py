"""
Представления проекта.
"""

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect, render

from .forms import LoginForm, RegisterForm


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
