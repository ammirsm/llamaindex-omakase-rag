__all__ = ["FolderSyncer"]

from datastore.services.syncer.folder.builder import FolderDocumentBuilder
from datastore.services.syncer.folder.loader import (
    FreshDocumentsMetaDataLoader,
    RelatedDocumentsObjectLoader,
)


class FolderSyncer(object):
    DOC_ID_FIELD = "file id"

    def __init__(self, folder):
        self.fresh_docs_meta_data_loader = FreshDocumentsMetaDataLoader(folder)
        self.related_docs_object_loader = RelatedDocumentsObjectLoader(folder)
        self.folder = folder

    def sync(self):
        self.fresh_docs_meta_data_loader.load_data()

        self.related_docs_object_loader.load_data()

        fresh_docs = self.fresh_docs_meta_data_loader.docs
        related_docs = self.related_docs_object_loader.docs

        for fresh_doc in fresh_docs:
            self.folder_document_builder = FolderDocumentBuilder(fresh_doc, related_docs, self.folder)
            self.folder_document_builder.build()

    def find_should_be_updated_meta_data(self, fresh_docs, related_docs):
        should_be_updated_meta_data = []
        for fresh_doc in fresh_docs:
            document_in_database = related_docs.filter(doc_id=fresh_doc[0])

            # Handle the case where the document is in the database
            if document_in_database.exists():
                should_be_updated_meta_data.append(fresh_doc)
