from __future__ import absolute_import, unicode_literals

import numpy as np
from celery import shared_task
from core.celery import app
from core.settings import EMBEDDING_MODEL
from django_celery_beat.models import PeriodicTask
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


@shared_task
def sync_folder(instance_uuid):
    """
    Syncs the folder with the given folder_id

    Args:
        instance_uuid: the uuid of the folder
    """
    from datastore.models import Folder

    try:
        # Get the folder and sync the related docs with source
        folder = Folder.objects.get(uuid=instance_uuid)
        folder.sync_related_docs_with_source()
    except Folder.DoesNotExist:
        # If the folder is not found, delete the periodic task
        PeriodicTask.objects.get(
            name=str(instance_uuid),
        ).delete()


@shared_task
def update_chunk_embedding(chunk_id):
    """
    Updates the chunk embedding for the given chunk_id

    Args:
        chunk_id: the id of the chunk
    """

    from datastore.models import DocumentChunk

    document_chunk = DocumentChunk.objects.get(id=chunk_id)
    if not np.any(document_chunk.embedding):
        embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)
        document_chunk.embedding = embed_model.get_text_embedding(text=document_chunk.chunk)
        document_chunk.save()


@app.task
def added_folder_periodic_tasks_checker():
    """
    This is just the safety check if someone used bulk_create function to update their folders, it will catch the
    updates and make sure the periodic tasks are up-to-date.
    """

    from datastore.models import Folder

    folders = Folder.objects.all()

    for folder in folders:
        folder.update_or_create_periodic_task()
