__all__ = ["SyncerFactory"]

from datastore.services.syncer.folder.syncer import FolderSyncer


class SyncerFactory(object):
    FOLDER = "folder"
    syncers = {FOLDER: FolderSyncer}

    @classmethod
    def get_syncer(cls, syncer_type):
        return cls.syncers[syncer_type]
