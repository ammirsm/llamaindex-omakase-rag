from core.base.models import BaseData
from core.settings import EMBEDDING_SIZE
from django.db import models
from llama_index.core import Document as LlamaDocument
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from pgvector.django import VectorField

from datastore.models.folder import Folder


class Document(BaseData):
    """
    Model for storing documents
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
        # TODO: 1
        # https://docs.llamaindex.ai/en/stable/module_guides/loading/node_parsers/modules.html#sentencesplitter
        # 1. chunk the document text based on chunk size
        # base_splitter = SentenceSplitter(chunk_size=512)
        # 2. save the chunks
        # documents (llamaindex) should be created from the actual text that we have here
        # nodes = splitter.get_nodes_from_documents(documents)

        splitter = SentenceSplitter(
            chunk_size=int(str(self.chunk_size)),
            chunk_overlap=int(str(self.chunk_overlap)),
        )
        nodes = splitter.get_nodes_from_documents([LlamaDocument(text=self.text)])
        for node in nodes:
            # TODO: Should Delete old chunks after update Document
            DocumentChunk.objects.get_or_create(document_id=self.id, chunk=node.text)

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
        # TODO 2:
        # https://docs.llamaindex.ai/en/stable/module_guides/models/embeddings.html
        # 1. create embeddings for the chunk
        # 2. save the embeddings
        if not self.embedding:
            embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
            self.embedding = embed_model.get_text_embedding(text=self.chunk)
            self.save()

    class Meta:
        verbose_name = "Document Chunk"
        verbose_name_plural = "Document Chunks"


# TODO 3: Make these post saves tasks -- do it together
