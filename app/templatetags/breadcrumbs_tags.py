"""
Хлебные крошки по имени маршрута и контексту шаблона.
"""

from django import template
from django.urls import NoReverseMatch, reverse

register = template.Library()

_MAX_TITLE = 52


def _short(title: str) -> str:
    title = (title or "").strip() or "…"
    if len(title) <= _MAX_TITLE:
        return title
    return title[: _MAX_TITLE - 1] + "…"


def _safe_reverse(name: str, **kwargs) -> str:
    try:
        return reverse(name, kwargs=kwargs) if kwargs else reverse(name)
    except NoReverseMatch:
        return "/"


def _item(title: str, *, url=None, is_current: bool = False) -> dict:
    return {"title": title, "url": url, "is_current": is_current}


@register.inclusion_tag("partials/breadcrumbs.html", takes_context=True)
def breadcrumbs(context):
    request = context.get("request")
    if request is None:
        return {"breadcrumb_items": [_item("Главная", url="/", is_current=True)]}

    match = getattr(request, "resolver_match", None)
    if match is None or not match.url_name:
        return {"breadcrumb_items": [_item("Главная", url="/", is_current=True)]}

    name = match.url_name
    kw = match.kwargs
    c = context

    def home():
        return _item("Главная", url="/", is_current=False)

    # — Главная (лендинг): крошки не показываем —
    if name == "landing":
        return {"breadcrumb_items": []}

    items: list[dict] = [home()]

    def add_current(title: str):
        items.append(_item(_short(title), url=None, is_current=True))

    # — Публичные страницы —
    if name == "about":
        add_current("О нас")
    elif name == "advantages":
        add_current("Преимущества")
    elif name == "security":
        add_current("Безопасность")
    elif name == "organizations":
        add_current("Для организаций")
    elif name == "contacts":
        add_current("Контакты")
    elif name == "feedback":
        add_current("Обратная связь")
    elif name == "faq":
        add_current("FAQ")
    elif name == "privacy":
        add_current("Политика конфиденциальности")
    elif name == "terms":
        add_current("Пользовательское соглашение")

    # — Материалы —
    elif name == "materials":
        add_current("Материалы")
    elif name == "material_detail":
        items.append(_item("Материалы", url=_safe_reverse("materials"), is_current=False))
        m = c.get("material")
        add_current(getattr(m, "title", None) or "Материал")
    elif name == "material_quiz_complete":
        items.append(_item("Материалы", url=_safe_reverse("materials"), is_current=False))
        add_current("Сохранение результата")

    # — Тесты знаний —
    elif name == "knowledge_tests":
        add_current("Тесты")
    elif name == "knowledge_test_detail":
        items.append(_item("Тесты", url=_safe_reverse("knowledge_tests"), is_current=False))
        t = c.get("test")
        add_current(getattr(t, "title", None) or "Тест")
    elif name == "knowledge_test_take_intro":
        items.append(_item("Тесты", url=_safe_reverse("knowledge_tests"), is_current=False))
        t = c.get("test")
        items.append(
            _item(
                _short(getattr(t, "title", None) or "Тест"),
                url=_safe_reverse("knowledge_test_detail", slug=kw.get("slug", "")),
                is_current=False,
            )
        )
        add_current("Начало теста")
    elif name == "knowledge_test_take":
        items.append(_item("Тесты", url=_safe_reverse("knowledge_tests"), is_current=False))
        t = c.get("test")
        items.append(
            _item(
                _short(getattr(t, "title", None) or "Тест"),
                url=_safe_reverse("knowledge_test_detail", slug=kw.get("slug", "")),
                is_current=False,
            )
        )
        add_current("Прохождение")
    elif name == "knowledge_test_result":
        items.append(_item("Тесты", url=_safe_reverse("knowledge_tests"), is_current=False))
        t = c.get("test")
        items.append(
            _item(
                _short(getattr(t, "title", None) or "Тест"),
                url=_safe_reverse("knowledge_test_detail", slug=kw.get("slug", "")),
                is_current=False,
            )
        )
        add_current("Результат")

    # — Учётная запись —
    elif name == "register":
        add_current("Регистрация")
    elif name == "login":
        add_current("Вход")

    # — Личный кабинет —
    elif name == "cabinet":
        add_current("Личный кабинет")
    elif name == "cabinet_materials":
        items.append(_item("Личный кабинет", url=_safe_reverse("cabinet"), is_current=False))
        add_current("Материалы в кабинете")
    elif name == "cabinet_tests":
        items.append(_item("Личный кабинет", url=_safe_reverse("cabinet"), is_current=False))
        add_current("Тесты в кабинете")
    elif name == "settings":
        add_current("Настройки")

    # — Админ-панель приложения —
    elif name == "admin_panel":
        add_current("Админ-панель")
    elif name == "admin_user_roles":
        items.append(_item("Админ-панель", url=_safe_reverse("admin_panel"), is_current=False))
        add_current("Роли пользователей")
    elif name == "admin_material_categories":
        items.append(_item("Админ-панель", url=_safe_reverse("admin_panel"), is_current=False))
        add_current("Категории материалов")
    elif name == "admin_material_statistics":
        items.append(_item("Админ-панель", url=_safe_reverse("admin_panel"), is_current=False))
        add_current("Статистика материалов")
    elif name == "admin_material_statistics_export":
        items.append(_item("Админ-панель", url=_safe_reverse("admin_panel"), is_current=False))
        items.append(
            _item(
                "Статистика материалов",
                url=_safe_reverse("admin_material_statistics"),
                is_current=False,
            )
        )
        add_current("Экспорт")
    elif name == "admin_feedback_submissions":
        items.append(_item("Админ-панель", url=_safe_reverse("admin_panel"), is_current=False))
        add_current("Обращения")
    elif name == "admin_feedback_detail":
        items.append(_item("Админ-панель", url=_safe_reverse("admin_panel"), is_current=False))
        items.append(
            _item(
                "Обращения",
                url=_safe_reverse("admin_feedback_submissions"),
                is_current=False,
            )
        )
        sub = c.get("submission")
        label = f"№ {kw.get('pk', '')}"
        if sub is not None:
            subj = (getattr(sub, "subject", None) or "").strip()
            if subj:
                label = _short(subj)
        add_current(label)

    # — Панель куратора —
    elif name == "curator_panel":
        add_current("Панель куратора")
    elif name == "curator_materials_manage":
        items.append(_item("Панель куратора", url=_safe_reverse("curator_panel"), is_current=False))
        add_current("Материалы")
    elif name == "curator_material_create":
        items.append(_item("Панель куратора", url=_safe_reverse("curator_panel"), is_current=False))
        items.append(
            _item("Материалы", url=_safe_reverse("curator_materials_manage"), is_current=False)
        )
        add_current("Новый материал")
    elif name == "curator_material_edit":
        items.append(_item("Панель куратора", url=_safe_reverse("curator_panel"), is_current=False))
        items.append(
            _item("Материалы", url=_safe_reverse("curator_materials_manage"), is_current=False)
        )
        m = c.get("material")
        add_current(getattr(m, "title", None) or "Редактирование материала")
    elif name == "curator_knowledge_tests_manage":
        items.append(_item("Панель куратора", url=_safe_reverse("curator_panel"), is_current=False))
        add_current("Тесты")
    elif name == "curator_knowledge_test_create":
        items.append(_item("Панель куратора", url=_safe_reverse("curator_panel"), is_current=False))
        items.append(
            _item("Тесты", url=_safe_reverse("curator_knowledge_tests_manage"), is_current=False)
        )
        add_current("Новый тест")
    elif name == "curator_knowledge_test_edit":
        items.append(_item("Панель куратора", url=_safe_reverse("curator_panel"), is_current=False))
        items.append(
            _item("Тесты", url=_safe_reverse("curator_knowledge_tests_manage"), is_current=False)
        )
        t = c.get("test")
        add_current(getattr(t, "title", None) or "Редактирование теста")
    elif name == "curator_knowledge_test_question_edit":
        items.append(_item("Панель куратора", url=_safe_reverse("curator_panel"), is_current=False))
        items.append(
            _item("Тесты", url=_safe_reverse("curator_knowledge_tests_manage"), is_current=False)
        )
        t = c.get("test")
        items.append(
            _item(
                _short(getattr(t, "title", None) or "Тест"),
                url=_safe_reverse("curator_knowledge_test_edit", slug=kw.get("slug", "")),
                is_current=False,
            )
        )
        add_current("Вопрос")
    elif name == "curator_knowledge_test_set_publish":
        items.append(_item("Панель куратора", url=_safe_reverse("curator_panel"), is_current=False))
        items.append(
            _item("Тесты", url=_safe_reverse("curator_knowledge_tests_manage"), is_current=False)
        )
        add_current("Публикация")

    else:
        tail = request.path.strip("/").split("/")[-1] if request.path.strip("/") else ""
        label = tail.replace("-", " ") if tail else "Страница"
        add_current(label)

    return {"breadcrumb_items": items}
