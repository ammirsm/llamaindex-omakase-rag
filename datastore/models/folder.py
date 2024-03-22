import json

from core.base.models import BaseModel
from django.db import models
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from datastore.models import Config
from datastore.services import SyncerFactory
from datastore.tasks import sync_folder


class Folder(BaseModel):
    """
    Model for storing folders
    """

    folder_id = models.CharField(max_length=1000)
    config = models.ForeignKey(Config, on_delete=models.CASCADE)

    # this needs to be updated regularly
    last_sync = models.DateTimeField(null=True, blank=True)
    cron_config = models.JSONField(default=dict, null=True, blank=True)
    sync_interval = models.IntegerField(default=5)

    def __str__(self):
        return self.folder_id

    def _get_syncer(self):
        """
        It will get the syncer from the factory for the Folder.
        """
        return SyncerFactory().get_syncer(SyncerFactory.FOLDER)(self)

    def sync_related_docs_with_source(self):
        """
        Syncs the folder with the given folder_id and update the related documents.
        """
        syncer = self._get_syncer()
        syncer.sync()

    def update_or_create_periodic_task(self):
        """
        Update or create the interval and periodic task for the folder.
        """

        # Create the interval schedule for the folder sync
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=self.sync_interval,
            period=IntervalSchedule.MINUTES,
        )

        # Create the periodic task for the folder sync
        PeriodicTask.objects.update_or_create(
            name=str(self.uuid),
            defaults={"interval": schedule, "task": sync_folder.name, "args": json.dumps([str(self.uuid)])},
        )

    def post_save(self):
        """
        Post save method for the folder
        """

        # After saving the folder we need to update or create the periodic tasks for the folder.
        self.update_or_create_periodic_task()

    class Meta:
        verbose_name = "Folder"
        verbose_name_plural = "Folders"
