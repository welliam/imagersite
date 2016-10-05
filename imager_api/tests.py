from django.test import TestCase
from django.contrib.auth.models import User
from factory.django import DjangoModelFactory, ImageField


class PhotoFactory(DjangoModelFactory):
    class Meta(object):
        model = Photo
    photo = ImageField()


class PhotoApiTestCase(TestCase):
    """Test case for Photo Api."""

    def setUp(self):
        """Setup for photo api testcase."""
        self.user = User(username='Bob')
        self.user.save()

        self.client.force_login(self.user)
        self.photo = PhotoFactory(
            user=self.user,
            title='A title',
        )
        self.photo.save()

