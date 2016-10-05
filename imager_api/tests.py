from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from factory.django import DjangoModelFactory, ImageField
from image.models import Photo
import json


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

    def test_status_code(self):
        """Test status is 200."""
        response = self.client.get(reverse('photo_api') + '.json')
        self.assertEqual(response.status_code, 200)
    
    def test_data_has_photo(self):
        """Test response had a photo and title."""
        response = self.client.get(reverse('photo_api') + '.json')
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data[0]['title'], self.photo.title)