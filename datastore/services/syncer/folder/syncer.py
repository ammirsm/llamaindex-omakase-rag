__all__ = ["FolderSyncer"]

from datastore.services.syncer.folder.builder import FolderDocumentBuilder
from datastore.services.syncer.folder.loader import FolderLoader


class FolderSyncer(object):
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
