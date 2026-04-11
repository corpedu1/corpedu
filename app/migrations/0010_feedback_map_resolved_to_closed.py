# Старый статус «Выполнено» (resolved) объединён с «Закрыто».

from django.db import migrations


def forwards(apps, schema_editor):
    FeedbackSubmission = apps.get_model("app", "FeedbackSubmission")
    FeedbackSubmission.objects.filter(status="resolved").update(status="closed")


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0009_alter_feedbacksubmission_id"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
