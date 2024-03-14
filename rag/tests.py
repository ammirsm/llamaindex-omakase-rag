from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from uac.models import FolderPermission, UACUser


class DocumentListViewTest(APITestCase):
    fixtures = ["datastore/tests/fixtures/datastore.json"]

    def setUp(self):
        from datastore.models import Folder

        self.user = UACUser.objects.create_user(username="test", password="test")
        self.folder = Folder.objects.first()
        self.client.force_login(self.user)

    def tearDown(self) -> None:
        self.client.logout()

    def test_folder_permission_required(self):
        url = reverse("rag:search-on-chunks")
        response = self.client.get(url, {"search": "test text"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_response(self):
        url = reverse("rag:search-on-chunks")
        FolderPermission.objects.create(user=self.user, folder=self.folder)
        response = self.client.get(url, {"search": "test text", "document__folder": self.folder.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data["results"][0]["distance"])
        self.assertTrue(response.data["results"][0]["distance"] >= response.data["results"][1]["distance"])
