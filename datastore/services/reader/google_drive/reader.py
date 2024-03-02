import logging
from typing import List

from llama_index.core.schema import Document
from llama_index.readers.google import GoogleDriveReader

logger = logging.getLogger(__name__)


class DjangoGoogleDriveReader(GoogleDriveReader):
    def load_file_meta_data(
        self,
        folder_id: str = None,
        mime_types: List[str] = None,
    ) -> List[Document]:
        """Load data from the folder id and file ids.

        Args:
            folder_id: folder id of the folder in google drive.
            file_ids: file ids of the files in google drive.
            mime_types: the mimeTypes you want to allow e.g.: "application/vnd.google-apps.document"
        Returns:
            List[Document]: A list of documents.
        """
        self._creds, self._drive = self._get_credentials()

        try:
            file_meta_datas = self._get_fileids_meta(folder_id=folder_id, mime_types=mime_types)

            file_meta_data_list = []

            for file_meta_data in file_meta_datas:
                file_meta_data_list.append(
                    {
                        "file id": file_meta_data[0],
                        "author": file_meta_data[1],
                        "file name": file_meta_data[2],
                        "mime type": file_meta_data[3],
                        "created at": file_meta_data[4],
                        "modified at": file_meta_data[5],
                    }
                )
            return file_meta_data_list
        except Exception as e:
            logger.error(f"An error occurred while loading from folder: {e}")

    def load_document_from_meta_data(self, meta_data: dict) -> List[Document]:
        self._creds, self._drive = self._get_credentials()

        fileid_meta_list = [
            meta_data["file id"],
            meta_data["author"],
            meta_data["file name"],
            meta_data["mime type"],
            meta_data["created at"],
            meta_data["modified at"],
        ]

        return self._load_data_fileids_meta([fileid_meta_list])
