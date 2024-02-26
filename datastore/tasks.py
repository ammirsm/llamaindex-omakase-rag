from celery import shared_task

from datastore.models import Folder


@shared_task
def sync_folder(instance_id):
    """
    Syncs the folder with the given folder_id
    """
    folder = Folder.objects.get(id=instance_id)
    folder.sync_related_docs_with_source()
