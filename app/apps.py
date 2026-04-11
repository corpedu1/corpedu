from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "app"
    verbose_name = "CyberLearn"

    def ready(self):
        # Регистрация тегов шаблонов (хлебные крошки)
        import app.templatetags.breadcrumbs_tags  # noqa: F401
