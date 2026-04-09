"""
Представления проекта.
"""

from django.shortcuts import render


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
    Отображает страницу «Регистрация».
    """
    return render(request, "register.html")


def login(request):
    """
    Отображает страницу «Вход».
    """
    return render(request, "login.html")
