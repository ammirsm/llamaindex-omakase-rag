"""
Script for seeding the database with dummy data
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django

django.setup()

LOCALHOST_URL = "http://localhost:8000"

# TODO: Login to local with the username and password

# TODO: Request local to make sure the api is working
