from datastore.services.syncer.base import BaseLoader


class FolderLoader(BaseLoader):
    def __init__(self, folder):
        self.folder = folder
        self.reader = self.folder.config.google_drive_reader()

    def _load_docs_from_reader(self):
        self.fresh_docs = self.reader.load_data(folder_id=self.folder.folder_id)

    def _load_related_docs(self):
        self.related_docs = self.folder.documents.all()

    def load_data(self):
        self._load_docs_from_reader()
        self._load_related_docs()
