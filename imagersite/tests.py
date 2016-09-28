from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core import mail
from factory.django import DjangoModelFactory, ImageField
from image.models import Photo


class PhotoFactory(DjangoModelFactory):
    class Meta(object):
        model = Photo
    photo = ImageField()


class AuthenticatedTestCase(TestCase):
    """Test cases inherit from this when they need a user.

    The client has methods for logging in; this is for testing the
    views associated with registration and log in."""

    def setUp(self):
        self.username = 'username'
        self.password = ':LSKDjfsd89s'
        self.email = 'email@example.org'
        csrf = self.get_csrf_token(reverse('registration_register'))
        self.client.post(reverse('registration_register'), dict(
            csrfmiddlewaretoken=csrf,
            username=self.username,
            password1=self.password,
            password2=self.password,
            email=self.email,
        ))
        url = mail.outbox[-1].body.split()[-1]
        path = '/'.join(url.split('/')[1:])
        self.client.get('/' + path)

    def get_csrf_token(self, url):
        """Get a csrf token for testing."""
        return self.client.get(url).context['csrf_token']

    def log_in(self, username=None, password=None):
        """Log user in.

        self.client has a login method, but this is used when the
        response of a successful login is needed."""
        csrf = self.get_csrf_token(reverse('auth_login'))
        username = username or self.username
        password = password or self.password
        return self.client.post(reverse('auth_login'), dict(
            username=username,
            password=password,
            csrfmiddlewaretoken=csrf
        ))


class HomeViewTestCase(TestCase):
    """Test case for home view."""

    def setUp(self):
        """Get the home directory and store the response."""
        self.response = self.client.get(reverse('home'))
        self.user = User(username='test')
        self.user.save()

    def test_home_view_status_code(self):
        """Test home view returns 200."""
        self.assertEqual(self.response.status_code, 200)

    def test_home_view_has_anchor(self):
        """Test home view has anchor tag."""
        self.assertContains(self.response, '</a>')

    def test_home_view_has_register_link(self):
        """Test home view has register link."""
        self.assertContains(
            self.response,
            'href="{}"'.format(reverse('registration_register'))
        )

    def test_home_view_has_login_link(self):
        """Test home view has login link."""
        self.assertContains(
            self.response,
            'href="{}"'.format(reverse('auth_login'))
        )

    def test_home_view_has_random_image(self):
        """Test home view has a random image."""
        PhotoFactory(user=self.user).save()
        self.client.get(reverse('home'))
        self.assertContains(
            self.response,
            '<img src='
        )

    def test_home_view_static_image(self):
        """Test home view has a random image."""
        self.assertContains(
            self.response,
            '<img src='
        )

    def test_home_view_random_image_in_context(self):
        """Test random image is in context."""
        self.assertIn("random_image_url", self.response.context)

    def auth_response(self):
        """Authenticated response."""
        self.client.force_login(self.user)
        return self.client.get(reverse('home'))

    def test_home_view_nonauth_nav_library(self):
        """Test home view does not link to library in nav bar."""
        expected = 'href="{}"'.format(reverse('library'))
        self.assertContains(self.response, expected, count=0)

    def test_home_view_nonauth_nav_profile(self):
        """Test home view does not link to library in nav bar."""
        expected = 'href="{}"'.format(reverse('library'))
        self.assertContains(self.response, expected, count=0)

    def test_home_view_auth_nav_library(self):
        """Test authenticated home view links to library in nav bar."""
        expected = 'href="{}"'.format(reverse('library'))
        self.assertContains(self.auth_response(), expected)

    def test_home_view_auth_nav_profile(self):
        """Test authenticated home view links to library in nav bar."""
        expected = 'href="{}"'.format(reverse('profile'))
        self.assertContains(self.auth_response(), expected)


class RegistrationViewTestCase(TestCase):
    """Test case for registration view."""

    def setUp(self):
        """Test registration view."""
        self.response = self.client.get(reverse('registration_register'))

    def test_register_view_status_code(self):
        """Test register view returns 200."""
        self.assertEqual(self.response.status_code, 200)

    def test_register_view_has_form(self):
        """Test register view has form."""
        self.assertContains(self.response, '</form>')

    def test_register_failure(self):
        """Test register with bad credentials."""
        self.assertEqual(
            self.client.post(reverse('registration_register'), {}).status_code,
            200
        )


class LoginViewTestCase(TestCase):
    """Test case for login view."""

    def setUp(self):
        """Test login view."""
        self.response = self.client.get(reverse('auth_login'))

    def test_register_view_status_code(self):
        """Test login view returns 200."""
        self.assertEqual(self.response.status_code, 200)

    def test_login_view_has_form(self):
        """Test login view has form."""
        self.assertContains(self.response, '</form>')


class RegisterTestCase(AuthenticatedTestCase):
    """Test case for registering users."""

    def test_register(self):
        """Test creating a user and saving."""
        self.assertTrue(bool(User.objects.filter(username=self.username)))

    def test_login(self):
        """Test login."""
        self.assertEqual(self.log_in().status_code, 302)

    def test_login_failure(self):
        """Test login failure."""
        self.client.get(reverse('auth_logout'))
        self.assertEqual(
            self.log_in(username=self.username + 'a').status_code,
            200
        )
