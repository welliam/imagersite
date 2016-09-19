from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
# Create your models here.


PUB_CHOICES = (
    ('Public', 'Public'),
    ('Private', 'Private'),
    ('Shared', 'Shared'),
)


def photo_path(instance, filename):
    """Create file path for the photo."""
    return "{0}/{1}".format(instance, filename)


@python_2_unicode_compatible
class Photo(models.Model):
    """Information about photo."""
    user = models.ForeignKey(
        User,
        on_delete=models.deletion.CASCADE,
        related_name='photos',
        null=True,
    )
    photo = models.ImageField(
        upload_to=photo_path,
        blank=True,
        null=True
    )
    title = models.CharField(max_length=128)
    description = models.TextField()
    date_uploaded = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)
    published = models.CharField(
        max_length=7,
        choices=PUB_CHOICES,
        default='Public'
    )


@python_2_unicode_compatible
class Album(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    user = models.ForeignKey(
        User,
        on_delete=models.deletion.CASCADE,
        related_name='albums'
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)
    published = models.CharField(
        max_length=7,
        choices=PUB_CHOICES,
        default='Public'
    )
