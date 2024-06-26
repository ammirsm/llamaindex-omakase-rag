# Generated by Django 4.2.9 on 2024-02-21 15:00

import uuid

import django.db.models.deletion
from django.db import migrations, models
from pgvector.django import VectorExtension


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        VectorExtension(),
        migrations.CreateModel(
            name="Config",
            fields=[
                (
                    "id",
                    models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("credentials", models.JSONField(default=dict)),
                ("token", models.JSONField(default=dict)),
                ("email", models.CharField(max_length=1000)),
            ],
            options={
                "verbose_name": "Config",
                "verbose_name_plural": "Configs",
            },
        ),
        migrations.CreateModel(
            name="Folder",
            fields=[
                (
                    "id",
                    models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("folder_id", models.CharField(max_length=1000)),
                ("config", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="datastore.config")),
            ],
            options={
                "verbose_name": "Folder",
                "verbose_name_plural": "Folders",
            },
        ),
        migrations.CreateModel(
            name="Document",
            fields=[
                (
                    "id",
                    models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("raw_data", models.JSONField(default=dict)),
                ("doc_id", models.CharField(max_length=1000)),
                ("excluded_embed_metadata_keys", models.JSONField(default=list)),
                ("excluded_llm_metadata_keys", models.JSONField(default=list)),
                ("extra_info", models.JSONField(default=dict)),
                ("hash", models.CharField(max_length=1000)),
                ("metadata", models.JSONField(default=dict)),
                ("metadata_template", models.TextField()),
                ("text", models.TextField()),
                ("text_template", models.TextField()),
                ("folder", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="datastore.folder")),
            ],
            options={
                "verbose_name": "Document",
                "verbose_name_plural": "Documents",
            },
        ),
    ]
