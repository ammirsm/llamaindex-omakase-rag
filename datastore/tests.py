from datetime import datetime, timezone

from core.settings import GDRIVE_SERVICE_ACCOUNT
from django.test import TestCase

from datastore.factories import ConfigFactory, FolderFactory
from datastore.models.config import Config


class TestConfig(TestCase):
    def test_config(self):
        # GIVEN create a config object
        config = Config.objects.create(credentials=GDRIVE_SERVICE_ACCOUNT, email="test@test.com")

        # THEN the config object should be created
        self.assertEqual(config.email, "test@test.com")


class TestFolder(TestCase):
    def test_sync(self):
        # GIVEN create a folder object
        config = ConfigFactory()
        folder = FolderFactory(config=config)

        # WHEN sync_related_docs_with_source is called
        folder.sync_related_docs_with_source()

        # THEN the folder should have 10 documents
        self.assertEqual(folder.documents.count(), 15)

        # WHEN Convert all the source_modified_at to old time to make sure they will be updated
        old_time = datetime(2015, 1, 1, 0, 0, 0, 0, timezone.utc)
        for doc in folder.documents.all():
            doc.source_modified_at = old_time
            doc.save()

        # WHEN sync_related_docs_with_source is called
        folder.sync_related_docs_with_source()

        # THEN all the source_modified_at should be updated
        for doc in folder.documents.all():
            self.assertNotEqual(doc.source_modified_at, old_time)
