from django.db import models
from django.utils.translation import gettext as _

# Create your models here.

class CreateDateTimeMixin(models.Model):
    """Add a created_at : DateTime field to a model"""

    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"), null=True)


class UpdateDateTimeMixin(models.Model):
    """Add an updated_at : DateTime field to a model"""

    class Meta:
        abstract = True

    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"), null=True)

class TimestampMixin(CreateDateTimeMixin, UpdateDateTimeMixin):
    """Add a created_at and updated_at : DateTime field to a model"""

    class Meta:
        abstract = True