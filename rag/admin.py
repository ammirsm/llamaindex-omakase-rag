from django.contrib import admin

from .models import RequestLogs


@admin.register(RequestLogs)
class RequestLogsAdmin(admin.ModelAdmin):
    list_display = ["request", "response", "status_code", "created_at"]
