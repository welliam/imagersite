from django.test import TestCase
from django.contrib.auth.models import User
from .models import Photo    
from datetime import datetime

# Create your tests here.

class PhotoTestCase(TestCase):
    """Test case for photo Model"""

    def setUp(self):
        """Setup photo model."""
        self.user = User(username='Cris', first_name='Cris')
        Photo(
            user=self.user, 
            title='image1.jpg',
            description='The first photo.'
        ).save()

    
    def test_photo_has_title(self):
        """Test photo has title."""
        self.assertEqual(self.user.photo.title, 'image1')

    def test_photo_has_descrip(self):
        """Test photo has a description."""
        self.assertEqual(self.user.photo.description, 'The first photo.')
    
    def test_photo_path(self):
        """Test the path of the file."""
        self.assertIn('/media/image1.jpg', self.user.photo.upload_to)

    def test_date_uploaded(self):
        """Test uploaded date."""
        date = datetime.utcnow().strftime("%Y-%m-%d")
        self.assertEqual(self.user.photo.date_uploaded, date)