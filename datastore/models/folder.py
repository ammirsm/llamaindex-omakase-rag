from core.base.models import BaseModel
from django.db import models

from datastore.models.config import Config
from datastore.services import SyncerFactory


class Folder(BaseModel):
    """
    Model for storing folders
    """

    folder_id = models.CharField(max_length=1000)
    config = models.ForeignKey(Config, on_delete=models.CASCADE)

    # this needs to be updated regularly
    last_sync = models.DateTimeField(null=True, blank=True)
    cron_config = models.JSONField(default=dict)

    def __str__(self):
        return self.folder_id

    def _get_syncer(self):
        return SyncerFactory().get_syncer(SyncerFactory.FOLDER)(self)

    def sync_related_docs_with_source(self):
        syncer = self._get_syncer()
        syncer.sync()

    class Meta:
        verbose_name = "Folder"
        verbose_name_plural = "Folders"
