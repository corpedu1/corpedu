# Заменяет цепочку 0012–0020: демо-контент загружается из fixture app/fixtures/ib_demo.json
# (без отдельных модулей seed_ib_content / seed_material_bodies).

from django.db import migrations


def _load_demo_fixture(apps, schema_editor):
    LearningMaterial = apps.get_model("app", "LearningMaterial")
    if LearningMaterial.objects.filter(slug="material-paroli-i-mfa").exists():
        return
    from django.core.management import call_command

    call_command("loaddata", "ib_demo", verbosity=0)


def _noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    replaces = [
        ("app", "0012_seed_ib_materials_and_tests"),
        ("app", "0013_assign_kurator_author"),
        ("app", "0014_expand_seed_material_bodies"),
        ("app", "0015_refresh_seed_material_bodies"),
        ("app", "0016_refresh_seed_material_bodies_again"),
        ("app", "0017_refresh_seed_material_bodies_v3"),
        ("app", "0018_refresh_seed_material_bodies_v4"),
        ("app", "0019_refresh_seed_material_bodies_v5"),
        ("app", "0020_refresh_seed_material_bodies_final"),
    ]

    dependencies = [
        ("app", "0011_alter_feedbacksubmission_status_choices"),
    ]

    operations = [
        migrations.RunPython(_load_demo_fixture, _noop),
    ]
