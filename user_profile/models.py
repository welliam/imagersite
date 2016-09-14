from __future__ import unicode_literals
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible


class ProfileManager(models.Manager):
    def get_queryset(self):
        queryset = super(ProfileManager, self).get_queryset()
        return queryset.filter(is_active=True)


@python_2_unicode_compatible
class UserProfile(models.Model):
    """Information for a user's profile."""
    user = models.OneToOneField(
        User,
        primary_key=True,
        on_delete=models.deletion.CASCADE,
        related_name='profile',
        unique=True
    )
    is_active = models.BooleanField()
    active = ProfileManager()

    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    camera_type = models.CharField(max_length=128)
    genre = models.CharField(max_length=128)
    is_professional = models.BooleanField(default=False)
    hireable = models.BooleanField(default=False)
    website = models.CharField(max_length=128)

    def __repr__(self):
        return 'UserProfile(first_name={})'.format(self.first_name)


@receiver(models.signals.post_save, sender=User)
def create_profile(sender, **kwargs):
    UserProfile(
        user=kwargs['instance'],
        is_active=False
    ).save()
