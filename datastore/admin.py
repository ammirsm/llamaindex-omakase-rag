from django.contrib import admin

from datastore.models.config import Config
from datastore.models.document import Document
from datastore.models.folder import Folder


class ConfigAdmin(admin.ModelAdmin):
    list_display = ("email", "created_at", "updated_at")
    search_fields = ("email",)
    list_filter = ("created_at", "updated_at")


class FolderAdmin(admin.ModelAdmin):
    list_display = ("folder_id", "config", "created_at", "updated_at")
    search_fields = ("folder_id", "config__email")
    list_filter = ("created_at", "updated_at")


class DocumentAdmin(admin.ModelAdmin):
    list_display = ("doc_id", "folder", "created_at", "updated_at")
    search_fields = ("doc_id", "folder__folder_id")
    list_filter = ("created_at", "updated_at")


admin.site.register(Config, ConfigAdmin)
admin.site.register(Folder, FolderAdmin)
admin.site.register(Document, DocumentAdmin)
