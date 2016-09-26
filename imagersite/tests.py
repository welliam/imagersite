from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core import mail


class AuthenticatedTestCase(TestCase):
    """Test cases inherit from this when they need a user."""

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

    def log_in(self):
        """Log user in.

        self.client has a login method, but this is used when the
        response of a successful login is needed."""
        csrf = self.get_csrf_token(reverse('auth_login'))
        return self.client.post(reverse('auth_login'), dict(
            username=self.username,
            password=self.password,
            csrfmiddlewaretoken=csrf
        ))


class HomeViewTestCase(TestCase):
    """Test case for home view."""

    def setUp(self):
        """Get the home directory and store the response."""
        self.response = self.client.get(reverse('home'))

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
