__all__ = ["DjangoGoogleDriveReader"]

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
    ) -> List[dict]:
        """
        Load data from the folder id and file ids.

        This method is responsible for loading file metadata from a specific Google Drive folder. It uses the Google
        Drive API to fetch the metadata of all files in the specified folder that match the provided MIME types.

        Args: folder_id (str, optional): The ID of the folder in Google Drive from which to load file metadata.
        Defaults to None. mime_types (List[str], optional): A list of MIME types to filter the files by. Only files
        that have a MIME type in this list will have their metadata loaded. Defaults to None.

        Returns:
            List[dict]: A list of dictionaries, each representing the metadata of a file. Each dictionary contains the
             following keys:
                - "file id": The ID of the file.
                - "author": The author of the file.
                - "file name": The name of the file.
                - "mime type": The MIME type of the file.
                - "created at": The creation date of the file.
                - "modified at": The last modification date of the file.

        Raises:
            Exception: If an error occurs while loading the file metadata from the folder, an error message is logged
            and the exception is raised.
        """
        # Get the credentials and drive
        self._creds, self._drive = self._get_credentials()

        try:
            # Get the file meta data
            file_meta_datas = self._get_fileids_meta(folder_id=folder_id, mime_types=mime_types)

            return [
                {
                    "file id": data[0],
                    "author": data[1],
                    "file name": data[2],
                    "mime type": data[3],
                    "created at": data[4],
                    "modified at": data[5],
                }
                for data in file_meta_datas
            ]
        except Exception as e:
            logger.error(f"An error occurred while loading from folder: {e}")

    def load_document_from_meta_data(self, metadata: dict) -> List[Document]:
        """
        This method is used to load a document from the provided metadata.

        Args:
            metadata (dict): A dictionary containing the metadata of the document. The dictionary should have the
            following keys:
                - "file id": The id of the file.
                - "author": The author of the file.
                - "file name": The name of the file.
                - "mime type": The mime type of the file.
                - "created at": The creation date of the file.
                - "modified at": The last modification date of the file.

        Returns:
            List[Document]: A list of Document objects loaded from the provided metadata.
        """
        # Get the credentials and drive
        self._creds, self._drive = self._get_credentials()

        # Get the file metadata and the order here is important because in the _load_data_fileids_meta it will be used
        fileid_meta_list = [
            metadata["file id"],
            metadata["author"],
            metadata["file name"],
            metadata["mime type"],
            metadata["created at"],
            metadata["modified at"],
        ]

        # Load the data from the file ids and return Document
        return self._load_data_fileids_meta([fileid_meta_list])
