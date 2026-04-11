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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('about/', views.about, name='about'),
    path('advantages/', views.advantages, name='advantages'),
    path('security/', views.security, name='security'),
    path('contacts/', views.contacts, name='contacts'),
    path('feedback/', views.feedback, name='feedback'),
    path('faq/', views.faq, name='faq'),
    path('materials/', views.materials, name='materials'),
    path('materials/<slug:slug>/quiz-complete/', views.material_quiz_complete, name='material_quiz_complete'),
    path('materials/<slug:slug>/', views.material_detail, name='material_detail'),
    path('tests/', views.knowledge_tests, name='knowledge_tests'),
    path('tests/<slug:slug>/take/<int:attempt_id>/', views.knowledge_test_take, name='knowledge_test_take'),
    path('tests/<slug:slug>/take/', views.knowledge_test_take_intro, name='knowledge_test_take_intro'),
    path('tests/<slug:slug>/result/<int:attempt_id>/', views.knowledge_test_result, name='knowledge_test_result'),
    path('tests/<slug:slug>/', views.knowledge_test_detail, name='knowledge_test_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('cabinet/materials/', views.cabinet_materials, name='cabinet_materials'),
    path('cabinet/tests/', views.cabinet_tests, name='cabinet_tests'),
    path('cabinet/', views.cabinet, name='cabinet'),
    path('settings/', views.settings, name='settings'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/user-roles/', views.admin_user_roles, name='admin_user_roles'),
    path('admin-panel/material-categories/', views.admin_material_categories, name='admin_material_categories'),
    path('admin-panel/material-statistics/', views.admin_material_statistics, name='admin_material_statistics'),
    path(
        'admin-panel/material-statistics/export/',
        views.admin_material_statistics_export,
        name='admin_material_statistics_export',
    ),
    path('admin-panel/feedback/', views.admin_feedback_submissions, name='admin_feedback_submissions'),
    path('admin-panel/feedback/<int:pk>/', views.admin_feedback_detail, name='admin_feedback_detail'),
    path('curator-panel/', views.curator_panel, name='curator_panel'),
    path('curator-panel/materials/', views.curator_materials_manage, name='curator_materials_manage'),
    path('curator-panel/materials/create/', views.curator_material_create, name='curator_material_create'),
    path('curator-panel/materials/<slug:slug>/', views.curator_material_edit, name='curator_material_edit'),
    path('curator-panel/tests/', views.curator_knowledge_tests_manage, name='curator_knowledge_tests_manage'),
    path('curator-panel/tests/create/', views.curator_knowledge_test_create, name='curator_knowledge_test_create'),
    path('curator-panel/tests/<slug:slug>/publish/', views.curator_knowledge_test_set_publish, name='curator_knowledge_test_set_publish'),
    path(
        'curator-panel/tests/<slug:slug>/edit/question/<int:question_id>/',
        views.curator_knowledge_test_question_edit,
        name='curator_knowledge_test_question_edit',
    ),
    path('curator-panel/tests/<slug:slug>/edit/', views.curator_knowledge_test_edit, name='curator_knowledge_test_edit'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
