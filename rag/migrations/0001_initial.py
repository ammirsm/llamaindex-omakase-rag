# Generated by Django 4.2.9 on 2024-02-21 15:00

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="RequestLogs",
            fields=[
                (
                    "id",
                    models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
                ),
                ("request", models.JSONField(default=dict)),
                ("response", models.JSONField(default=dict)),
                ("status_code", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "RequestLog",
                "verbose_name_plural": "RequestLogs",
            },
        ),
    ]
