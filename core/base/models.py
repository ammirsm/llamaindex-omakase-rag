import uuid

from django.db import models


class Active(models.Model):
    """
    Mixin for active models
    """

    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class UUID(models.Model):
    """
    Mixin for UUID models
    """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class DateTime(models.Model):
    """
    Mixin for DateTime models
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModel(Active, UUID, DateTime):
    """
    Base model for all models
    """

    class Meta:
        abstract = True


class BaseData(BaseModel):
    """
    Base model for all data models
    """

    raw_data = models.JSONField(default=dict)

    class Meta:
        abstract = True
