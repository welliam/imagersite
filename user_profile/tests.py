from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile

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
