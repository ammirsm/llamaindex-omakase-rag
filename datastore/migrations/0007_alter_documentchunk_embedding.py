# Generated by Django 4.2.9 on 2024-03-03 23:41

from django.db import migrations
import pgvector.django


class Migration(migrations.Migration):
    dependencies = [
        ("datastore", "0006_document_chunk_overlap_document_chunk_size_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="documentchunk",
            name="embedding",
            field=pgvector.django.VectorField(dimensions=384, null=True),
        ),
    ]
