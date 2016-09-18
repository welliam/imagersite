from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
# Create your models here.

def photo_path(instance, filename):
    """Create file path for the photo."""
    return "{0}/{1}".format(instance, filename)

@python_2_unicode_compatible
class Photo(models.Model):
    """Information about photo."""
    photo = models.ImageField(
        upload_to = photo_path,
        blank=True,
        null=True
    )
    title = models.CharField(max_length=128)
    description = models.TextField()
