from django.test import TestCase
from django.contrib.auth.models import User
from .models import Album, Photo
from datetime import datetime


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
        self.assertEqual(
            self.user.photos.first().description, 'The first photo.'
        )

    # def test_photo_path(self):
    #     """Test the path of the file."""
    #     self.assertIn('/media/image1.jpg', self.user.photos.first().photo.upload_to)

    def test_date_uploaded(self):
        """Test uploaded date."""
        format_string = "%Y-%m-%d"
        expected_date = datetime.utcnow().strftime(format_string)
        date = self.user.photos.first().date_uploaded.strftime(format_string)
        self.assertEqual(expected_date, date)

    def test_published_public(self):
        """Test published is public."""
        self.assertEqual(self.user.photos.first().published, 'Public')

    def test_published_set_private(self):
        """Test published gets set to private."""
        photo = self.user.photos.first()
        photo.published = 'Private'
        photo.save()
        self.assertEqual(self.user.photos.first().published, 'Private')


class AlbumTestCase(TestCase):
    """Test case for album model."""

    def setUp(self):
        """Setup Album test case."""
        self.user = User(username='Cris', first_name='Cris')
        self.user.save()

        self.photo = Photo(
            user=self.user,
            title='some photo',
            description='this is a photo'
        )
        self.photo.save()

        self.album = Album(
            title='good album',
            description='this is an album',
            user=self.user
        )
        self.album.save()

    def test_album_title(self):
        """Test album title field."""
        self.assertTrue(hasattr(self.album, 'title'))

    def test_user_foreign_key(self):
        """Test album user field."""
        self.assertEqual(
            self.album.title, self.album.user.albums.first().title
        )

    def test_album_date_created(self):
        """Test album date created field."""
        format_string = "%Y-%m-%d"
        expected_date = datetime.utcnow().strftime(format_string)
        date = self.album.date_created.strftime(format_string)
        self.assertEqual(expected_date, date)

    def test_published(self):
        """Test published field."""
        self.assertEqual(self.album.published, 'Public')
