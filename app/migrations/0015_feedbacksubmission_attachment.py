import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0014_demo_seed_admin_charts"),
    ]

    operations = [
        migrations.AddField(
            model_name="feedbacksubmission",
            name="attachment",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="feedback/attachments/",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=("pdf", "doc", "docx", "png", "jpg", "jpeg", "txt", "zip"),
                        message="Допустимые форматы: PDF, DOC, DOCX, PNG, JPG, JPEG, TXT, ZIP.",
                    )
                ],
                verbose_name="Вложение",
            ),
        ),
    ]
