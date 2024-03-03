# Generated by Django 4.2.9 on 2024-02-29 15:04

from django.db import migrations, models
import django.db.models.deletion
import pgvector.django
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("datastore", "0005_auto_20240229_0521"),
    ]

    operations = [
        migrations.AddField(
            model_name="document",
            name="chunk_overlap",
            field=models.IntegerField(default=20),
        ),
        migrations.AddField(
            model_name="document",
            name="chunk_size",
            field=models.IntegerField(default=1000),
        ),
        migrations.CreateModel(
            name="DocumentChunk",
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
                ("chunk", models.TextField()),
                ("embedding", pgvector.django.VectorField(dimensions=384)),
                (
                    "document",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="chunks", to="datastore.document"
                    ),
                ),
            ],
            options={
                "verbose_name": "Document Chunk",
                "verbose_name_plural": "Document Chunks",
            },
        ),
    ]