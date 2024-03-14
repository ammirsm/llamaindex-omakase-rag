from core.settings import EMBEDDING_MODEL
from datastore.models import DocumentChunk
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from pgvector.django import L2Distance
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from uac.permissions import HasFolderPermission

from .serializers import DocumentChunkSerializer

search = openapi.Parameter("search", openapi.IN_QUERY, description="search text", type=openapi.TYPE_STRING)


class DocumentListView(ListAPIView):
    serializer_class = DocumentChunkSerializer
    queryset = DocumentChunk.objects.all()
    permission_classes = [IsAuthenticated, HasFolderPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "document__folder",
    ]

    @swagger_auto_schema(manual_parameters=[search])
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        text = self.request.query_params.get("search", None)
        if text:
            embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)
            text_embedding = embed_model.get_text_embedding(text=text)

            queryset = queryset.annotate(distance=L2Distance("embedding", text_embedding)).order_by("distance")
        return queryset
