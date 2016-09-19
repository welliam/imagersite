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
        self.user.save()
        Photo(
            user=self.user, 
            title='image1',
            description='The first photo.'
        ).save()

    
    def test_photo_has_title(self):
        """Test photo has title."""
        self.assertEqual(self.user.photos.first().title, 'image1')

    def test_photo_has_descrip(self):
        """Test photo has a description."""
        self.assertEqual(self.user.photos.first().description, 'The first photo.')
    
    # def test_photo_path(self):
    #     """Test the path of the file."""
    #     self.assertIn('/media/image1.jpg', self.user.photos.first().photo.upload_to)

    def test_date_uploaded(self):
        """Test uploaded date."""
        format_string = "%Y-%m-%d"
        expected_date = datetime.utcnow().strftime(format_string)
        date = self.user.photos.first().date_uploaded.strftime(format_string)
        self.assertEqual(expected_date, date)