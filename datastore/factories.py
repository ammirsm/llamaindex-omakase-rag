from core.base.factory import BaseModelFactory
from core.settings import GDRIVE_SERVICE_ACCOUNT, GDRIVE_TEST_FOLDER_ID

from datastore.models import Config, Folder


class ConfigFactory(BaseModelFactory):
    class Meta:
        model = Config

    credentials = GDRIVE_SERVICE_ACCOUNT
    email = "test@test.com"


class FolderFactory(BaseModelFactory):
    class Meta:
        model = Folder

    folder_id = GDRIVE_TEST_FOLDER_ID
    config = ConfigFactory()


class DocumentFactory(BaseModelFactory):
    class Meta:
        model = "datastore.Document"

    folder = FolderFactory()


class DocumentChunkFactory(BaseModelFactory):
    class Meta:
        model = "datastore.DocumentChunk"

    document = DocumentFactory()
