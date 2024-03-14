from datastore.models import DocumentChunk
from rest_framework import serializers


class DocumentChunkSerializer(serializers.ModelSerializer):
    distance = serializers.CharField(read_only=True)

    class Meta:
        model = DocumentChunk
        fields = ["id", "chunk", "distance", "document"]
        read_only_fields = [
            "distance",
        ]
