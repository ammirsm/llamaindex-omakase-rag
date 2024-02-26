from core.base.models import BaseModel
from django.db import models


class Config(BaseModel):
    """
    Model for storing configuration of google drive
    """

    credentials = models.JSONField(default=dict)
    token = models.JSONField(default=dict)
    email = models.CharField(max_length=1000)

    def __str__(self):
        return self.email

    def google_drive_reader(self):
        from llama_index.readers.google import GoogleDriveReader

        reader = GoogleDriveReader(credentials_path=self.credentials)
        return reader

    class Meta:
        verbose_name = "Config"
        verbose_name_plural = "Configs"
