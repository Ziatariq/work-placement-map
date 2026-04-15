from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("facilities", "0003_facilityrequirement_notes_and_programs"),
    ]

    operations = [
        migrations.AlterField(
            model_name="facility",
            name="latitude",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="facility",
            name="longitude",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
