import json

import requests
from core.settings import LOGIN_PASSWORD, LOGIN_USERNAME
from datastore.models import Folder
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Demonstrates the use of IntegrityError"

    def handle(self, *args, **kwargs):
        LOCALHOST_URL = "http://localhost:8000"

        url = f"{LOCALHOST_URL}/api/token/login/"

        payload = json.dumps({"username": LOGIN_USERNAME, "password": LOGIN_PASSWORD})
        headers = {"accept": "application/json", "Content-Type": "application/json"}

        response = requests.request("POST", url, headers=headers, data=payload)

        access_token = json.loads(response.text)["access"]

        document_folder = Folder.objects.last()

        url = f"{LOCALHOST_URL}/rag/search_on_chunks/?document__folder={document_folder.id}&search=text"

        headers = {"accept": "application/json", "Authorization": f"Bearer {access_token}"}

        response = requests.request("GET", url, headers=headers, data={})

        print(response.text)
