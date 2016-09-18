from django.test import TestCase
from django.contrib.auth import User
from .models import Photo    

# Create your tests here.

class PhotoTestCase(TestCase):
    """Test case for photo Model"""

    def setUp(self):
        """Setup photo model."""
        self.user = User(username='Cris', first_name='Cris')
        Photo(
            user=self.user, 
            title='image1',
            description='The first photo.'
        ).save()

    
    def test_photo_has_title(self):
        """Test photo has title."""
        self.assertEqual(self.user.photo.title, 'image1')

    def test_photo_has_descrip(self):
        """Test photo has a description."""
        self.assertEqual(self.user.photo.description, 'The first photo.')
    