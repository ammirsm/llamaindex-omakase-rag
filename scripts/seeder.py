"""
Script for seeding the database with dummy data
"""

import os

from core.settings import GDRIVE_SERVICE_ACCOUNT, GDRIVE_TEST_FOLDER_ID

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django

django.setup()

from uac.models import UACUser
from datastore.models.config import Config
from datastore.models.folder import Folder
from datastore.models import Document


# Remove everything from database
Document.objects.all().delete()
Folder.objects.all().delete()
Config.objects.all().delete()
# UACUser.objects.all().delete()


# Import django user
UACUser.objects.create_superuser("new_admin_4", password="123admin123", email="new_admin@user.com")

# Create the config

config = Config.objects.create(credentials=GDRIVE_SERVICE_ACCOUNT, email="test@test.com")

# Create the folder

folder = Folder.objects.create(folder_id=GDRIVE_TEST_FOLDER_ID, config=config)

# Create the documents
folder.sync_related_docs_with_source()
