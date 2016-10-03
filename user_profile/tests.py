from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserProfile
from imagersite.tests import AuthenticatedTestCase


# Create your tests here.
class ProfileTestCase(TestCase):
    """TestCase for Profile"""

    def setUp(self):
        """Set up User Profile"""
        self.user = User(username='Cris', first_name='Cris')
        self.user.save()

    def test_user_has_profile(self):
        """Test User has a profile."""
        self.assertTrue(hasattr(self.user, 'profile'))

    def test_profile_username(self):
        """Test Profile has username"""
        self.assertEqual(self.user.profile.user.username, 'Cris')

# Learn to paramertize

    def test_profile_has_cameratype(self):
        """Test profile has cameria type attr."""
        self.assertTrue(hasattr(self.user.profile, 'camera_type'))

    def test_profile_repr(self):
        """Test repr function."""
        self.assertIn('Cris', repr(self.user.profile))

    def test_profile_active(self):
        """Test profile manager."""
        self.assertTrue(len(UserProfile.active.all()) > 0)


class UserProfilePageTestCase(AuthenticatedTestCase):
    """Test case for viewing the profile."""

    def test_profile_page(self):
        self.log_in()
        self.assertEqual(self.client.get('/profile/').status_code, 200)

    def test_profile_page_has_username(self):
        self.log_in()
        self.assertIn(
            self.username.encode('utf-8'),
            self.client.get('/profile/').content
        )

    def test_profile_page_has_photo_count(self):
        self.log_in()
        self.assertIn(
            b'Photos uploaded:',
            self.client.get('/profile/').content
        )

    def test_profile_page_has_album_count(self):
        self.log_in()
        self.assertIn(b'Albums created:', self.client.get('/profile/').content)


class EditProfileTestCase(TestCase):
    """Edit profile test case."""

    def setUp(self):
        """GET the route named edit_profile."""
        self.user = User(username='test')
        self.user.save()
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('edit_profile'))

    def test_status_code(self):
        """Test the status code for GETing edit_profile is 200."""
        self.assertEqual(self.response.status_code, 200)

    def test_edit_profile(self):
        """Test editing a album stores the updated value."""
        new_camera_type = 'camera'
        data = {
            'camera_type': new_camera_type,
        }
        response = self.client.post(reverse('edit_profile'), data)
        self.assertEqual(response.status_code, 302)
        profile = UserProfile.objects.filter(user=self.user).first()
        self.assertEqual(profile.camera_type, new_camera_type)
