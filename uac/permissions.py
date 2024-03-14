from datastore.models import Folder
from rest_framework import permissions


class HasFolderPermission(permissions.BasePermission):
    """
    Permission to check if user has permission to view folder details
    """

    def has_permission(self, request, view):
        folder_id = request.GET.get("document__folder")
        try:
            folder = Folder.objects.get(id=folder_id)
        except Folder.DoesNotExist:
            return False

        return folder.folderpermission_set.filter(user=request.user).exists()
