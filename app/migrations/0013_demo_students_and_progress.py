# Демо-студенты (роль «Сотрудник») с осмысленными ФИО, прогресс по материалам и тестам.

from django.db import migrations
from django.utils import timezone


def _complete_material_quizzes(
    LearningMaterial, MaterialPage, UserMaterialPageQuizCompletion, UserMaterialProgress, user, material_slug
):
    try:
        material = LearningMaterial.objects.get(slug=material_slug)
    except LearningMaterial.DoesNotExist:
        return
    pages = list(MaterialPage.objects.filter(material=material).order_by("order", "id"))
    if not pages:
        return
    for page in pages:
        has_quiz = bool(
            page.quiz_question
            and str(page.quiz_question).strip()
            and page.quiz_correct in (1, 2, 3, 4)
        )
        if has_quiz:
            UserMaterialPageQuizCompletion.objects.get_or_create(
                user=user,
                page=page,
                defaults={"selected_choice": page.quiz_correct},
            )
    UserMaterialProgress.objects.update_or_create(
        user=user,
        material=material,
        defaults={"last_page_index": len(pages)},
    )


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


def forwards(apps, schema_editor):
    User = apps.get_model("app", "User")
    LearningMaterial = apps.get_model("app", "LearningMaterial")
    MaterialPage = apps.get_model("app", "MaterialPage")
    UserMaterialPageQuizCompletion = apps.get_model("app", "UserMaterialPageQuizCompletion")
    UserMaterialProgress = apps.get_model("app", "UserMaterialProgress")
    KnowledgeTest = apps.get_model("app", "KnowledgeTest")
    KnowledgeTestQuestion = apps.get_model("app", "KnowledgeTestQuestion")
    KnowledgeTestAnswerChoice = apps.get_model("app", "KnowledgeTestAnswerChoice")
    KnowledgeTestAttempt = apps.get_model("app", "KnowledgeTestAttempt")
    KnowledgeTestAttemptAnswer = apps.get_model("app", "KnowledgeTestAttemptAnswer")

    demo_password = "StudentDemo2026!"

    students = (
        ("smirnova_anna", "Анна", "Смирнова", "anna.smirnova@demo.cyberlearn.local"),
        ("volkov_dmitry", "Дмитрий", "Волков", "dmitry.volkov@demo.cyberlearn.local"),
        ("kozlova_elena", "Елена", "Козлова", "elena.kozlova@demo.cyberlearn.local"),
        ("novikov_igor", "Игорь", "Новиков", "igor.novikov@demo.cyberlearn.local"),
        ("orlova_maria", "Мария", "Орлова", "maria.orlova@demo.cyberlearn.local"),
    )

    created_users = []
    for username, first_name, last_name, email in students:
        if User.objects.filter(username=username).exists():
            created_users.append(User.objects.get(username=username))
            continue
        user = User.objects.create_user(
            username=username,
            email=email,
            password=demo_password,
            first_name=first_name,
            last_name=last_name,
            role="employee",
        )
        created_users.append(user)

    anna, dmitry, elena, igor, maria = created_users

    # Анна: два материала полностью, один тест на 80%
    _complete_material_quizzes(
        LearningMaterial,
        MaterialPage,
        UserMaterialPageQuizCompletion,
        UserMaterialProgress,
        anna,
        "material-paroli-i-mfa",
    )
    _complete_material_quizzes(
        LearningMaterial,
        MaterialPage,
        UserMaterialPageQuizCompletion,
        UserMaterialProgress,
        anna,
        "material-fishing",
    )
    _complete_knowledge_test(
        KnowledgeTest,
        KnowledgeTestQuestion,
        KnowledgeTestAnswerChoice,
        KnowledgeTestAttempt,
        KnowledgeTestAttemptAnswer,
        anna,
        "test-osnovy-ib",
        80,
    )

    # Дмитрий: два платформенных теста (разные баллы)
    _complete_knowledge_test(
        KnowledgeTest,
        KnowledgeTestQuestion,
        KnowledgeTestAnswerChoice,
        KnowledgeTestAttempt,
        KnowledgeTestAttemptAnswer,
        dmitry,
        "test-pd-i-konfidencialnost",
        92,
    )
    _complete_knowledge_test(
        KnowledgeTest,
        KnowledgeTestQuestion,
        KnowledgeTestAnswerChoice,
        KnowledgeTestAttempt,
        KnowledgeTestAttemptAnswer,
        dmitry,
        "test-set-i-perimetr",
        76,
    )

    # Елена: один материал и один тест
    _complete_material_quizzes(
        LearningMaterial,
        MaterialPage,
        UserMaterialPageQuizCompletion,
        UserMaterialProgress,
        elena,
        "material-checklist-pisem",
    )
    _complete_knowledge_test(
        KnowledgeTest,
        KnowledgeTestQuestion,
        KnowledgeTestAnswerChoice,
        KnowledgeTestAttempt,
        KnowledgeTestAttemptAnswer,
        elena,
        "test-kontrol-dostupa",
        88,
    )

    # Игорь: три материала
    for slug in ("material-public-wifi", "material-chistyy-stol", "material-rezervnoe-kopirovanie"):
        _complete_material_quizzes(
            LearningMaterial,
            MaterialPage,
            UserMaterialPageQuizCompletion,
            UserMaterialProgress,
            igor,
            slug,
        )

    # Мария: один материал, два теста
    _complete_material_quizzes(
        LearningMaterial,
        MaterialPage,
        UserMaterialPageQuizCompletion,
        UserMaterialProgress,
        maria,
        "material-paroli-i-mfa",
    )
    _complete_knowledge_test(
        KnowledgeTest,
        KnowledgeTestQuestion,
        KnowledgeTestAnswerChoice,
        KnowledgeTestAttempt,
        KnowledgeTestAttemptAnswer,
        maria,
        "test-osnovy-ib",
        95,
    )
    _complete_knowledge_test(
        KnowledgeTest,
        KnowledgeTestQuestion,
        KnowledgeTestAnswerChoice,
        KnowledgeTestAttempt,
        KnowledgeTestAttemptAnswer,
        maria,
        "test-pd-i-konfidencialnost",
        72,
    )


def backwards(apps, schema_editor):
    User = apps.get_model("app", "User")
    usernames = (
        "smirnova_anna",
        "volkov_dmitry",
        "kozlova_elena",
        "novikov_igor",
        "orlova_maria",
    )
    User.objects.filter(username__in=usernames).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0012_seed_demo_content"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
