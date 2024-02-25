from django.contrib import admin

from .models import FolderPermission, UACUser


class UACUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "date_joined", "last_login")
    search_fields = ("username", "email")
    list_filter = ("is_staff", "is_active")


class FolderPermissionAdmin(admin.ModelAdmin):
    list_display = ("folder", "user", "created_at", "updated_at")
    search_fields = ("folder__folder_id", "user__username")
    list_filter = ("created_at", "updated_at")


admin.site.register(UACUser, UACUserAdmin)
admin.site.register(FolderPermission, FolderPermissionAdmin)
