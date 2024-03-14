from core.base.models import BaseModel
from datastore.models import Folder
from django.contrib.auth.models import AbstractUser
from django.db import models


class UACUser(AbstractUser):
    """
    Model for storing user details and inhertied from django base user model
    """

    def __str__(self):
        return self.username


class FolderPermission(BaseModel):
    """
    Model for storing folder permissions
    """

    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    user = models.ForeignKey(UACUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"user: {self.user}, folder: {self.folder}"

    class Meta:
        verbose_name = "FolderPermission"
        verbose_name_plural = "FolderPermissions"
