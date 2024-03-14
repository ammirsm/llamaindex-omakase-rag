from datetime import datetime, timezone

from core.settings import GDRIVE_SERVICE_ACCOUNT, GDRIVE_TEST_FOLDER_ID, IS_CIRCLE_CI
from core.utils import enable_celery_tasks
from django.test import TestCase
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from datastore.factories import ConfigFactory, FolderFactory
from datastore.models import Config, Document, DocumentChunk, Folder


class TestConfig(TestCase):
    def test_config(self):
        # GIVEN create a config object
        config = Config.objects.create(credentials=GDRIVE_SERVICE_ACCOUNT, email="test@test.com")

        # THEN the config object should be created
        self.assertEqual(config.email, "test@test.com")


class TestFolder(TestCase):
    def test_sync(self):
        if IS_CIRCLE_CI:
            return

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

    def test_periodic_task_created(self):
        # GIVEN we have a folder and config
        config = Config.objects.create(credentials=GDRIVE_SERVICE_ACCOUNT, email="test@test.com")
        folder = Folder.objects.create(folder_id=GDRIVE_TEST_FOLDER_ID, config=config)

        # THEN the interval schedule should be created
        self.assertTrue(
            IntervalSchedule.objects.filter(
                every=folder.sync_interval,
                period=IntervalSchedule.MINUTES,
            ).exists()
        )

        # THEN the periodic task should be created
        self.assertTrue(
            PeriodicTask.objects.filter(
                name=str(folder.uuid),
            ).exists()
        )


class DocumentTestCase(TestCase):
    DOC_ID = "test_doc"

    def setUp(self):
        with enable_celery_tasks():
            # GIVEN we have a folder and config
            config = Config.objects.create(credentials=GDRIVE_SERVICE_ACCOUNT, email="test@test.com")
            self.folder = Folder.objects.create(folder_id=GDRIVE_TEST_FOLDER_ID, config=config)

            # WHEN we create a document
            self.document = Document.objects.create(
                doc_id=self.DOC_ID,
                folder=self.folder,
                text="This is a test document.",
                metadata_template="{}",
                text_template="{}",
            )

    def test_document_creation(self):
        # THEN the document should be created
        document = Document.objects.get(doc_id=self.DOC_ID)
        self.assertEqual(document.text, "This is a test document.")

    def test_document_chunk_creation(self):
        # THEN the document should have chunks
        document = Document.objects.get(doc_id="test_doc")
        chunks = DocumentChunk.objects.filter(document=document)
        self.assertTrue(chunks.exists())

    def test_document_chunk_embeddings(self):
        # WHEN we have a document
        document = Document.objects.get(doc_id="test_doc")

        # THEN the document should have chunks and embeddings
        chunks = DocumentChunk.objects.filter(document=document)
        for chunk in chunks:
            self.assertIsNotNone(DocumentChunk.objects.get(id=chunk.id).embedding)

    def tearDown(self):
        Folder.objects.all().delete()
