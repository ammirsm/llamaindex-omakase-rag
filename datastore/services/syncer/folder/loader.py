from datastore.services.syncer.base import BaseLoader


class FreshDocumentsMetaDataLoader(BaseLoader):
    def __init__(self, folder):
        self.folder = folder
        self.reader = self.folder.config.google_drive_reader()

    def load_data(self):
        self.docs = self.reader.load_file_meta_data(folder_id=self.folder.folder_id)


class RelatedDocumentsObjectLoader(BaseLoader):
    def __init__(self, folder):
        self.folder = folder
        self.reader = self.folder.config.google_drive_reader()

    def load_data(self):
        self.docs = self.folder.documents.all()
