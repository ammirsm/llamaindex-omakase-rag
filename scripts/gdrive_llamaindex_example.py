from llama_index.readers.google import GoogleDriveReader

from core.settings import GDRIVE_SERVICE_ACCOUNT

loader = GoogleDriveReader(credentials_path=GDRIVE_SERVICE_ACCOUNT)


def load_data(folder_id: str):
    docs = loader.load_data(folder_id=folder_id)
    for doc in docs:
        doc.id_ = doc.metadata["file name"]
    return docs


documents = load_data(folder_id="1NIGvjHBuUQHWnMqzboyg-zLI1q_bOuCH")
