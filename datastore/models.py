from core.base.models import BaseData, BaseModel
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


class Folder(BaseModel):
    """
    Model for storing folders
    """

    folder_id = models.CharField(max_length=1000)
    config = models.ForeignKey(Config, on_delete=models.CASCADE)

    # this needs to be updated regularly
    last_sync = models.DateTimeField(auto_now=True)
    cron_config = models.JSONField(default=dict)

    def __str__(self):
        return self.name

    def sync_folder(self):
        """
        This function should connect to google drive with the config and load data from the folder

        Returns:

        """
        reader = self.config.google_drive_reader()
        reader.load_data(folder_id=self.folder_id)

    class Meta:
        verbose_name = "Folder"
        verbose_name_plural = "Folders"


class Document(BaseData):
    """
    Model for storing documents
    """

    doc_id = models.CharField(max_length=1000)
    excluded_embed_metadata_keys = models.JSONField(default=list)
    excluded_llm_metadata_keys = models.JSONField(default=list)
    extra_info = models.JSONField(default=dict)
    hash = models.CharField(max_length=1000)
    metadata = models.JSONField(default=dict)
    metadata_template = models.TextField()
    text = models.TextField()
    text_template = models.TextField()
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)

    def __str__(self):
        return self.doc_id

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
