from django.db import migrations

from remo_app.remo.models import Dataset


def rename_datasets(apps, schema_editor):
    for dataset in Dataset.objects.all():
        dataset.rename()


class Migration(migrations.Migration):

    dependencies = [
        ('remo', '0014_agrerrors'),
    ]

    operations = [
        migrations.RunPython(rename_datasets)
    ]
