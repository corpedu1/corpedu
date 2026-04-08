"""
Представления проекта.
"""

from django.shortcuts import render


def landing(request):
    """
    Отображает главную страницу веб-сервиса.
    """
    return render(request, "landing.html")
