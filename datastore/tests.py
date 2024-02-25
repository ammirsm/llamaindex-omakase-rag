from core.settings import GDRIVE_SERVICE_ACCOUNT, GDRIVE_TEST_FOLDER_ID
from django.test import TestCase

from datastore.models import Config


# Create your tests here.
class TestPassbook(TestCase):
    def test_config(self):
        config = Config.objects.create(credentials=GDRIVE_SERVICE_ACCOUNT, email="test@test.com")

        self.assertEqual(config.email, "test@test.com")

        google_drive_reader = config.google_drive_reader()

        docs = google_drive_reader.load_data(folder_id=GDRIVE_TEST_FOLDER_ID)

        for doc in docs:
            doc.id_ = doc.metadata["file name"]
        print(docs)
