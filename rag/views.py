# TODO 4: make an APIViewset for Retrival of RAG
# 1. it will get the actual query from the user and the folder that they want to search on
# 2. It will check if the user have the permission with FolderPermission model (make django permission class)
# 3. it will convert it to embedding (this is exactly what we have in the document chunker post save)
# 4. it will search the database for similar embeddings
# https://github.com/pgvector/pgvector-python?tab=readme-ov-file#django
# from pgvector.django import L2Distance
# Item.objects.order_by(L2Distance('embedding', THE DOCUMENT WHICH WE GOT EMBEDDING from ))[:5]
# 5. it will return the results to the user in a paginated way with the most similar results first
# 6. it will also log the request and the response in the database

from datastore.models.document import DocumentChunk
from django_filters.rest_framework import DjangoFilterBackend
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from pgvector.django import L2Distance
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView

from .serializers import DocumentChunkSerializer


class DocumentListView(ListAPIView):
    serializer_class = DocumentChunkSerializer
    queryset = DocumentChunk.objects.all()
    # permission_classes = [IsAuthenticated, ] #todo permission to folder
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "document",
        "document__folder",
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        text = self.request.query_params.get("text", None)
        if text:
            embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
            text_embedding = embed_model.get_text_embedding(text=text)

            queryset = queryset.annotate(distance=L2Distance("embedding", text_embedding)).order_by(
                L2Distance("embedding", text_embedding)
            )[:5]
        else:
            raise ValidationError("You should send 'text' for search in data")
        return queryset
