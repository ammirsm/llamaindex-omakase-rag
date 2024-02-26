# Generated by Django 4.2.9 on 2024-02-25 22:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("datastore", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="folder",
            name="cron_config",
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name="folder",
            name="last_sync",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="document",
            name="folder",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="documents", to="datastore.folder"
            ),
        ),
    ]