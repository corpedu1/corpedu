# Обновление choices поля status (без статуса «Выполнено»).

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0010_feedback_map_resolved_to_closed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedbacksubmission",
            name="status",
            field=models.CharField(
                choices=[
                    ("new", "Новая"),
                    ("in_progress", "В работе"),
                    ("closed", "Закрыто"),
                ],
                db_index=True,
                default="new",
                max_length=20,
                verbose_name="Статус",
            ),
        ),
    ]
