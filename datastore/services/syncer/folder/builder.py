from datetime import datetime, timezone

from datastore.services.syncer.base import BaseBuilder


class FolderDocumentBuilder(BaseBuilder):
    MODIFIED_AT_FIELD = "modified at"
    CREATED_AT_FIELD = "created at"
    DOC_ID_FIELD = "file id"

    def __init__(self, fresh_doc, related_docs, folder):
        self.fresh_doc = fresh_doc
        self.related_docs = related_docs
        self.folder = folder

    def build(self):
        document_in_database = self.related_docs.filter(doc_id=self.fresh_doc[self.DOC_ID_FIELD])

        # Handle the case where the document is in the database
        if document_in_database.exists():
            # If the document is in the database, create it
            self._update_doc(self.fresh_doc, document_in_database.first())
        else:
            # If the document is not in the database, create it
            self._create_doc(self.fresh_doc)

    def _create_doc(self, fresh_doc):
        from datastore.models import Document

        fresh_doc = self.folder.config.reader.load_document_from_meta_data(fresh_doc)
        fresh_doc = fresh_doc[0]

        doc = Document.objects.create(
            doc_id=fresh_doc.doc_id,
            excluded_embed_metadata_keys=fresh_doc.excluded_embed_metadata_keys,
            excluded_llm_metadata_keys=fresh_doc.excluded_llm_metadata_keys,
            extra_info=fresh_doc.extra_info,
            hash=fresh_doc.hash,
            metadata_template=fresh_doc.metadata_template,
            text_template=fresh_doc.text_template,
            text=fresh_doc.text,
            source_created_at=self._get_created_at_of_doc(fresh_doc),
            source_modified_at=self._get_modified_at_of_doc(fresh_doc),
            metadata=fresh_doc.metadata,
            folder=self.folder,
        )
        doc.save()
        pass

    def _update_doc(self, fresh_doc, doc_in_db):
        if self._is_modified(fresh_doc, doc_in_db):
            self._update_db_document_base_on_fresh_doc(fresh_doc, doc_in_db)

    def _update_db_document_base_on_fresh_doc(self, fresh_doc, doc_in_db):
        fresh_doc = self.folder.config.reader.load_document_from_meta_data(fresh_doc)
        fresh_doc = fresh_doc[0]

        doc_in_db.metadata = fresh_doc.metadata
        doc_in_db.text = fresh_doc.text
        doc_in_db.source_modified_at = self._get_modified_at_of_doc(fresh_doc)
        doc_in_db.extra_info = fresh_doc.extra_info
        doc_in_db.save(update_fields=["metadata", "text", "source_modified_at", "extra_info"])

    def _is_modified(self, new_doc, doc):
        fresh_doc_modified_at = self._get_modified_at_of_doc(new_doc)
        doc_in_db_modified_at = doc.source_modified_at

        if fresh_doc_modified_at and doc_in_db_modified_at:
            return fresh_doc_modified_at > doc_in_db_modified_at

        return False

    def _convert_to_datetime(self, date_string):
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        date_object = datetime.strptime(date_string, date_format)
        date_object = date_object.replace(tzinfo=timezone.utc)
        return date_object

    def _get_modified_at_of_doc(self, doc):
        if type(doc) is dict:
            metadata_value = doc[self.MODIFIED_AT_FIELD]
        else:
            metadata_value = doc.metadata[self.MODIFIED_AT_FIELD]
        return self._convert_to_datetime(metadata_value)

    def _get_created_at_of_doc(self, doc):
        if type(doc) is dict:
            metadata_value = doc[self.CREATED_AT_FIELD]
        else:
            metadata_value = doc.metadata[self.CREATED_AT_FIELD]
        return self._convert_to_datetime(metadata_value)
