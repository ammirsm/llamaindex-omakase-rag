from django.db import models


# Create your models here.
class RequestLogs(models.Model):
    """
    Model for storing request logs for debugging and tracking

    It can be used for caching the request and response.
    """

    request = models.JSONField(default=dict)
    response = models.JSONField(default=dict)
    status_code = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.request

    class Meta:
        verbose_name = "RequestLog"
        verbose_name_plural = "RequestLogs"
