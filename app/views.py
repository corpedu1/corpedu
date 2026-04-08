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
