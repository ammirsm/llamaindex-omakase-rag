from datastore.factories import DocumentChunkFactory
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class DocumentListViewTest(APITestCase):
    def setUp(self):
        self.document_chunk1 = DocumentChunkFactory()

    def test_get_queryset(self):
        url = reverse("rag:search-on-chunks")
        response = self.client.get(url, {"text": "test text"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
