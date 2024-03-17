"""
Script for seeding the database with dummy data
"""

from core.settings import GDRIVE_SERVICE_ACCOUNT, GDRIVE_TEST_FOLDER_ID, LOGIN_PASSWORD, LOGIN_USERNAME
from datastore.models import Config, Document, Folder
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from uac.models import FolderPermission, UACUser


class Command(BaseCommand):
    help = "This will add seed data to your database"

    def handle(self, *args, **kwargs):
        try:
            # Remove everything from database
            Document.objects.all().delete()
            Folder.objects.all().delete()
            Config.objects.all().delete()
            print("Deleted all documents, folders and configs")

            # Import django user
            try:
                UACUser.objects.create_superuser(
                    LOGIN_USERNAME, password=LOGIN_PASSWORD, email="new_admin@user.com"
                )
                print("Created superuser")
            except IntegrityError:
                pass

            # Create the config
            config = Config.objects.create(credentials=GDRIVE_SERVICE_ACCOUNT, email="test@test.com")
            print("Created config")

            # Create the folder
            folder = Folder.objects.create(folder_id=GDRIVE_TEST_FOLDER_ID, config=config)
            print("Created folder")

            # Create the documents
            print("Syncing related documents with source...")
            folder.sync_related_docs_with_source()
            print("Synced related documents with source")

            # Give user permission
            user = UACUser.objects.get(username=LOGIN_USERNAME)
            FolderPermission.objects.create(user=user, folder=folder)
            print("Gave user permission")

            print("Seeding completed successfully")
            print(f"Login with username: {LOGIN_USERNAME} and password: {LOGIN_PASSWORD}")
            print(f"Folder which has been synced is https://drive.google.com/drive/folders/{GDRIVE_TEST_FOLDER_ID}")

        except IntegrityError:
            self.stdout.write(self.style.ERROR("An IntegrityError occurred."))
