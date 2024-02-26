from core.base.models import BaseData
from django.db import models

from datastore.models.folder import Folder


class Document(BaseData):
    """
    Model for storing documents
    """

    doc_id = models.CharField(max_length=1000, db_index=True)
    excluded_embed_metadata_keys = models.JSONField(default=list)
    excluded_llm_metadata_keys = models.JSONField(default=list)
    extra_info = models.JSONField(default=dict)
    hash = models.CharField(max_length=1000)
    metadata = models.JSONField(default=dict)
    metadata_template = models.TextField()
    text = models.TextField()
    text_template = models.TextField()
    folder = models.ForeignKey(Folder, related_name="documents", on_delete=models.CASCADE)
    source_created_at = models.DateTimeField(null=True, blank=True)
    source_modified_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.doc_id

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
