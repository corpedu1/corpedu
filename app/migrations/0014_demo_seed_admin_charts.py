# Дополнительные демо-данные: плотнее распределение баллов по тестам и «стартов» материалов для графиков админки.

from django.db import migrations
from django.utils import timezone


def _complete_knowledge_test(
    KnowledgeTest,
    KnowledgeTestQuestion,
    KnowledgeTestAnswerChoice,
    KnowledgeTestAttempt,
    KnowledgeTestAttemptAnswer,
    user,
    test_slug,
    score_percent,
):
    try:
        test = KnowledgeTest.objects.get(slug=test_slug, is_published=True)
    except KnowledgeTest.DoesNotExist:
        return
    questions = list(KnowledgeTestQuestion.objects.filter(test=test).order_by("order", "id"))
    if not questions:
        return
    passed = score_percent >= test.passing_score_percent
    attempt = KnowledgeTestAttempt.objects.create(
        user=user,
        test=test,
        completed_at=timezone.now(),
        score_percent=score_percent,
        is_passed=passed,
    )
    for q in questions:
        correct = KnowledgeTestAnswerChoice.objects.filter(question=q, is_correct=True).first()
        if correct is None:
            continue
        KnowledgeTestAttemptAnswer.objects.create(
            attempt=attempt,
            question=q,
            selected_choice=correct,
        )


def _ensure_started(user, material_slug, LearningMaterial, UserMaterialProgress):
    try:
        material = LearningMaterial.objects.get(slug=material_slug)
    except LearningMaterial.DoesNotExist:
        return
    UserMaterialProgress.objects.get_or_create(
        user=user,
        material=material,
        defaults={"last_page_index": 1},
    )


def forwards(apps, schema_editor):
    User = apps.get_model("app", "User")
    LearningMaterial = apps.get_model("app", "LearningMaterial")
    UserMaterialProgress = apps.get_model("app", "UserMaterialProgress")
    KnowledgeTest = apps.get_model("app", "KnowledgeTest")
    KnowledgeTestQuestion = apps.get_model("app", "KnowledgeTestQuestion")
    KnowledgeTestAnswerChoice = apps.get_model("app", "KnowledgeTestAnswerChoice")
    KnowledgeTestAttempt = apps.get_model("app", "KnowledgeTestAttempt")
    KnowledgeTestAttemptAnswer = apps.get_model("app", "KnowledgeTestAttemptAnswer")

    # Идемпотентность: повторный прогон не дублирует попытки с тем же «маркером».
    if KnowledgeTestAttempt.objects.filter(
        user__username="volkov_dmitry",
        test__slug="test-osnovy-ib",
        score_percent=12,
    ).exists():
        return

    def u(name):
        try:
            return User.objects.get(username=name)
        except User.DoesNotExist:
            return None

    anna = u("smirnova_anna")
    dmitry = u("volkov_dmitry")
    elena = u("kozlova_elena")
    igor = u("novikov_igor")
    maria = u("orlova_maria")

    materials_for_starts = (
        "material-paroli-i-mfa",
        "material-checklist-pisem",
        "material-fishing",
        "material-public-wifi",
        "material-chistyy-stol",
        "material-rezervnoe-kopirovanie",
    )

    if dmitry:
        for slug in materials_for_starts:
            _ensure_started(dmitry, slug, LearningMaterial, UserMaterialProgress)
    if elena:
        for slug in (
            "material-paroli-i-mfa",
            "material-fishing",
            "material-public-wifi",
            "material-chistyy-stol",
            "material-rezervnoe-kopirovanie",
        ):
            _ensure_started(elena, slug, LearningMaterial, UserMaterialProgress)
    if igor:
        for slug in ("material-paroli-i-mfa", "material-fishing", "material-checklist-pisem"):
            _ensure_started(igor, slug, LearningMaterial, UserMaterialProgress)
    if maria:
        for slug in (
            "material-fishing",
            "material-checklist-pisem",
            "material-public-wifi",
            "material-chistyy-stol",
            "material-rezervnoe-kopirovanie",
        ):
            _ensure_started(maria, slug, LearningMaterial, UserMaterialProgress)

    extra_attempts = (
        (dmitry, "test-osnovy-ib", 12),
        (dmitry, "test-osnovy-ib", 18),
        (elena, "test-osnovy-ib", 25),
        (elena, "test-set-i-perimetr", 33),
        (igor, "test-pd-i-konfidencialnost", 42),
        (igor, "test-kontrol-dostupa", 58),
        (maria, "test-set-i-perimetr", 15),
        (anna, "test-pd-i-konfidencialnost", 38),
        (anna, "test-kontrol-dostupa", 52),
        (dmitry, "test-kontrol-dostupa", 68),
        (elena, "test-pd-i-konfidencialnost", 74),
        (igor, "test-osnovy-ib", 81),
        (maria, "test-kontrol-dostupa", 48),
        (dmitry, "test-set-i-perimetr", 55),
        (elena, "test-osnovy-ib", 88),
        (igor, "test-set-i-perimetr", 92),
        (maria, "test-osnovy-ib", 22),
        (dmitry, "test-pd-i-konfidencialnost", 28),
        (elena, "test-kontrol-dostupa", 45),
        (igor, "test-kontrol-dostupa", 65),
    )

    for user, test_slug, score in extra_attempts:
        if user is None:
            continue
        _complete_knowledge_test(
            KnowledgeTest,
            KnowledgeTestQuestion,
            KnowledgeTestAnswerChoice,
            KnowledgeTestAttempt,
            KnowledgeTestAttemptAnswer,
            user,
            test_slug,
            score,
        )


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0013_demo_students_and_progress"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
