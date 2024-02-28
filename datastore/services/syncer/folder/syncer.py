__all__ = ["FolderSyncer"]

from datastore.services.syncer.folder.builder import FolderDocumentBuilder
from datastore.services.syncer.folder.loader import FolderLoader


class FolderSyncer(object):
    DOC_ID_FIELD = "file id"

    def __init__(self, folder):
        self.folder_loader = FolderLoader(folder)
        self.folder = folder

    def sync(self):
        self.folder_loader.load_data()

        fresh_docs = self.folder_loader.fresh_docs
        related_docs = self.folder_loader.related_docs

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
