from core.base.models import BaseData
from core.settings import EMBEDDING_SIZE
from django.db import models
from llama_index.core import Document as LlamaDocument
from llama_index.core.node_parser import SentenceSplitter
from pgvector.django import VectorField

from datastore.models.folder import Folder


class Document(BaseData):
    """
    Model for storing documents from the folder
    """

    doc_id = models.CharField(max_length=1000, db_index=True)
    excluded_embed_metadata_keys = models.JSONField(default=list)
    excluded_llm_metadata_keys = models.JSONField(default=list)
    extra_info = models.JSONField(default=dict)
    hash = models.CharField(max_length=1000)
    metadata = models.JSONField(default=dict)
    metadata_template = models.TextField()
    text = models.TextField()
    text_template = models.TextField()
    folder = models.ForeignKey(Folder, related_name="documents", on_delete=models.CASCADE)
    source_created_at = models.DateTimeField(null=True, blank=True)
    source_modified_at = models.DateTimeField(null=True, blank=True)
    chunk_size = models.IntegerField(default=1000)
    chunk_overlap = models.IntegerField(default=20)

    def __str__(self):
        return self.doc_id

    def post_save(self):
        # Create the chunks for the document
        new_nodes = self._extract_nodes_from_new_document()

        # Get previous nodes
        previous_nodes = self._get_nodes()

        # Update the nodes
        self._update_nodes(new_nodes, previous_nodes)

    def _get_nodes(self):
        """
        Get the nodes of the related DocumentChunks
        """

        all_document_chunks = DocumentChunk.objects.filter(document_id=self.id)
        return list(all_document_chunks.values_list("chunk", flat=True))

    def _update_nodes(self, new_nodes, previous_nodes):
        """
        Update the nodes of the document based on the new nodes and previous nodes
        Args:
            new_nodes: the nodes that we need to be in the database
            previous_nodes: the nodes that are currently in the database
        """
        # Find which nodes should be created
        should_be_removed_nodes = list(set(previous_nodes) - set(new_nodes))
        # Remove the nodes that should be removed
        for node in should_be_removed_nodes:
            DocumentChunk.objects.filter(document_id=self.id, chunk=node).delete()
        # Find which nodes should be created
        should_be_created_nodes = list(set(new_nodes) - set(previous_nodes))
        # Create the nodes that should be created
        for node in should_be_created_nodes:
            DocumentChunk.objects.get_or_create(document_id=self.id, chunk=node)

    def _extract_nodes_from_new_document(self):
        splitter = SentenceSplitter(
            chunk_size=int(str(self.chunk_size)),
            chunk_overlap=int(str(self.chunk_overlap)),
        )
        nodes = splitter.get_nodes_from_documents([LlamaDocument(text=self.text)])
        nodes = [node.text for node in nodes]
        return nodes

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"


class DocumentChunk(BaseData):
    """
    Model for storing document chunks
    """

    chunk = models.TextField()
    document = models.ForeignKey(Document, related_name="chunks", on_delete=models.CASCADE)
    embedding = VectorField(dimensions=EMBEDDING_SIZE, null=True)

    def __str__(self):
        return str(self.id)

    def post_save(self):
        from datastore.tasks import update_chunk_embedding

        # Update the embedding for the chunk
        update_chunk_embedding.delay(self.id)

    class Meta:
        verbose_name = "Document Chunk"
        verbose_name_plural = "Document Chunks"
