from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from factory.django import DjangoModelFactory, ImageField
from image.models import Photo


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

    def test_stats_code(self):
        """Test status is 200."""
        response = self.client.get(reverse('photo_api') + '.json')
        self.assertEqual(response.status_code, 200)
    
