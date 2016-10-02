from datetime import datetime
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from factory.django import DjangoModelFactory, ImageField
from .models import Album, Photo
from django.db import transaction


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

    def test_library_links_to_album(self):
        """Test library page has links to images."""
        for album in self.user.albums.all():
            url = reverse('album', args=[album.pk])
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
        response = self.client.get(reverse('images', args=[999999]))
        self.assertContains(response, 'Photo not found')

    def test_photo_view_has_edit_link(self):
        link = reverse('edit_photo', args=[self.photo.pk])
        self.assertContains(self.response, 'href="{}"'.format(link))



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

    def test_album_view_nonexistent_album(self):
        response = self.client.get(reverse('album', args=[999999]))
        self.assertContains(response, 'Album not found')

    def test_album_view_has_edit_link(self):
        link = reverse('edit_album', args=[self.album.pk])
        self.assertContains(self.response, 'href="{}"'.format(link))


class CreateAlbumTestCase(UserTestCase):
    """Test case for creating albums."""

    def setUp(self):
        """Create a setup."""
        super(CreateAlbumTestCase, self).setUp()
        self.response = self.client.get(reverse('add_album'))

    def test_get_create_url(self):
        """Test getting create url."""
        self.assertEqual(self.response.status_code, 200)

    def test_form_rendered(self):
        """Test for is rendering on page."""
        self.assertContains(self.response, "</form>")

    def test_post_form(self):
        """Test post redirects correctly."""
        data = {
            'title': 'YeahWhatever',
            'description': 'Text',
            'published': 'Public',
        }
        response = self.client.post(reverse('add_album'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.albums.last().title, data['title'])

    def test_album_create_page_301(self):
        """Test create photo page returns 301 for unauthenticated user."""
        self.client.logout()
        response = self.client.get(reverse('add_photo'))
        self.assertEqual(response.status_code, 302)


class CreatePhotoTestCase(UserTestCase):
    """Add Photo test case."""

    def setUp(self):
        """Create a setup."""
        super(CreatePhotoTestCase, self).setUp()
        self.response = self.client.get(reverse('add_photo'))

    def test_status_code(self):
        """Test status code of add photo view."""
        self.assertEqual(self.response.status_code, 200)

    def test_form_rendered(self):
        """Test form is rendered to html."""
        self.assertContains(self.response, '</form>')

    def test_post_photo_form(self):
        """Test photo redirects and posts."""
        ct = self.response.context['csrf_token']
        data = {
            'csrf_token': ct,
            'title': 'TestPhoto',
            'description': 'Test Description.',
            'published': 'Public',
            'photo': PhotoFactory(user=self.user).photo.read(),
        }
        response = self.client.post(reverse('add_photo'), data)
        self.assertEqual(response.status_code, 302)
        new_photo = Photo.objects.last()
        self.assertEqual(new_photo.title, data['title'])
        self.assertTrue(new_photo.user is not None)

    def test_photo_create_page_301(self):
        """Test create photo page returns 301 for unauthenticated user."""
        self.client.logout()
        response = self.client.get(reverse('add_photo'))
        self.assertEqual(response.status_code, 302)


class EditPhotoTestCase(UserTestCase):
    """Edit photo test case."""

    def setUp(self):
        """Set up a photo to be edited."""
        super(EditPhotoTestCase, self).setUp()
        self.photo = self.user.photos.last()
        self.url = reverse('edit_photo', args=[self.photo.pk])
        self.response = self.client.get(self.url)

    def test_status_code(self):
        """Test status code of edit photo view."""
        self.assertEqual(self.response.status_code, 200)

    def test_edit_photo(self):
        """Test editing a photo stores the updated value."""
        new_title = self.photo.title + '!'
        data = {
            'title': new_title,
            'published': 'Public'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.photos.last().title, new_title)


class EditAlbumTestCase(UserTestCase):
    """Edit album test case."""

    def setUp(self):
        """Set up a album to be edited."""
        super(EditAlbumTestCase, self).setUp()
        self.album = self.user.albums.last()
        self.url = reverse('edit_album', args=[self.album.pk])
        self.response = self.client.get(self.url)

    def test_status_code(self):
        """Test status code of response."""
        self.assertEqual(self.response.status_code, 200)

    def test_edit_album(self):
        """Test editing a album stores the updated value."""
        new_title = self.album.title + '?!'
        data = {
            'title': new_title,
            'published': 'Shared',
            'photos': [p.pk for p in self.album.photos.all()]
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.albums.last().title, new_title)

    def test_add_photo_from_other_user(self):
        """Test that users cannot add a photo from another user."""
        other_user = User(username='whoever')
        other_user.save()
        p = PhotoFactory(user=other_user)
        p.save()
        data = dict(photos=[p.pk], title='album', published='Public')
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)

    def test_set_cover_not_in_photos(self):
        """Test that users cannot set a cover not in the album's photos."""
        p1 = self.user.photos.first()
        p2 = self.user.photos.last()
        self.assertNotEqual(p1, p2)  # test is useless otherwise
        data = dict(cover=p1.pk, title='album', photos=[p2.pk], published='Public')
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)

    def test_set_cover_from_other_user(self):
        """Test that users cannot set a cover from another user."""
        other_user = User(username='whoever')
        other_user.save()
        p = PhotoFactory(user=other_user)
        p.save()
        data = dict(cover=p.pk, title='album', published='Public')
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
