"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('feedback/', views.feedback, name='feedback'),
    path('faq/', views.faq, name='faq'),
    path('materials/', views.materials, name='materials'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('settings/', views.settings, name='settings'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/user-roles/', views.admin_user_roles, name='admin_user_roles'),
    path('admin-panel/material-categories/', views.admin_material_categories, name='admin_material_categories'),
    path('curator-panel/', views.curator_panel, name='curator_panel'),
    path('curator-panel/materials/create/', views.curator_material_create, name='curator_material_create'),
    path('admin/', admin.site.urls),
]
