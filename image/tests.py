from datetime import datetime
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from factory.django import DjangoModelFactory, ImageField
from .models import Album, Photo


class PhotoFactory(DjangoModelFactory):
    class Meta(object):
        model = Photo
    photo = ImageField()


class PhotoTestCase(TestCase):
    """Test case for photo Model"""

    def setUp(self):
        """Setup photo model."""
        self.user = User(username='Cris', first_name='Cris')
        self.user.save()
        PhotoFactory(
            user=self.user,
            title='image1',
            description='The first photo.',
        ).save()

    def test_photo_has_title(self):
        """Test photo has title."""
        self.assertEqual(self.user.photos.first().title, 'image1')

    def test_photo_has_descrip(self):
        """Test photo has a description."""
        self.assertEqual(
            self.user.photos.first().description, 'The first photo.'
        )

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

        self.album.photos.add(self.photo)

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

    def test_photos_foreign_key(self):
        """Test album photos field."""
        self.assertEqual(
            self.photo.title, self.album.photos.first().title
        )

    def test_album_cover(self):
        """Test album cover foreign key."""
        self.album.cover = self.photo
        self.album.save()
        self.assertEqual(
            self.photo.title,
            self.photo.cover_for.first().cover.title
        )


class UserTestCase(TestCase):
    """Testcase with a user."""

    def setUp(self, test_url=None):
        """Setup Library testcase."""
        self.user = User(username='acutebird')
        self.user.save()
        self.client.force_login(self.user)
        for i in range(10):
            PhotoFactory(
                user=self.user,
                title='image{}'.format(i),
                description='Descrpition for image{}'.format(i),
            ).save()
        album = Album(
            user=self.user,
            title='Blue Pictures',
            description='A test album.'
        )
        album.save()
        for photo in list(self.user.photos.all())[:3]:
            album.photos.add(photo)


class LibraryTestCase(UserTestCase):
    """Testcase for Library."""
    def setUp(self):
        super(LibraryTestCase, self).setUp()
        self.response = self.client.get(reverse('library'))

    def test_library_status_code(self):
        """Test status code of library page."""
        self.assertEqual(self.response.status_code, 200)

    def test_library_shows_images(self):
        """Test library page shows images."""
        self.assertContains(self.response, 'src="/media/cache')

    def test_library_links_to_image(self):
        """Test library page has links to images."""
        for photo in self.user.photos.all():
            url = reverse('images', args=[photo.pk])
            self.assertContains(self.response, url)


class PhotoViewTestCase(UserTestCase):
    """Test case for viewing a single image."""

    def setUp(self):
        """Set up for testing an photo."""
        super(PhotoViewTestCase, self).setUp()
        self.photo = self.user.photos.last()
        url = reverse('images', args=[self.photo.pk])
        self.response = self.client.get(url)

    def test_photo_view_response(self):
        self.assertEqual(self.response.status_code, 200)

    def test_photo_view_has_title(self):
        self.assertContains(self.response, self.photo.title)

    def test_photo_view_has_description(self):
        self.assertContains(self.response, self.photo.description)

    def test_photo_view_nonexistent_photo(self):
        response = self.client.get(reverse('images', args=[999]))
        self.assertContains(response, 'Photo not found')


class AlbumViewTestCase(UserTestCase):
    """Test case for viewing an album."""

    def setUp(self):
        """Set up for testing an album."""
        super(AlbumViewTestCase, self).setUp()
        self.album = self.user.albums.last()
        url = reverse('album', args=[self.album.pk])
        self.response = self.client.get(url)

    def test_album_view_response(self):
        """Test GETing album has status code 200."""
        self.assertEqual(self.response.status_code, 200)

    def test_album_has_album_title(self):
        """Test album contains album title."""
        self.assertContains(self.response, self.album.title)

    def test_album_has_album_description(self):
        """Test album contains album description."""
        self.assertContains(self.response, self.album.description)

    def test_album_displays_images(self):
        """Test album contains associated images."""
        for image in self.album.photos.all():
            self.assertContains(self.response, image.photo.url)
