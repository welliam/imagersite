from __future__ import unicode_literals
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible


class ProfileManager(models.Manager):
    """Manager for profiles.

    Only returns profiles for which the corresponding user's is_active
    field is True."""

    def get_queryset(self):
        """Return a queryset which only contains is_active user)."""
        queryset = super(ProfileManager, self).get_queryset()
        return queryset.filter(user__is_active__exact=True)


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
    objects = models.Manager()
    active = ProfileManager()

    camera_type = models.CharField(max_length=128, blank=True)
    genre = models.CharField(max_length=128, blank=True)
    is_professional = models.BooleanField(default=False)
    hireable = models.BooleanField(default=False)
    website = models.CharField(max_length=128, blank=True)

    def __repr__(self):
        return 'UserProfile(first_name={})'.format(self.user.first_name)


@receiver(models.signals.post_save, sender=User)
def create_profile(sender, **kwargs):
    """Create a new profile for a newly-created User."""
    UserProfile(
        user=kwargs['instance']
    ).save()
