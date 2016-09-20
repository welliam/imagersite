from django.test import TestCase, Client


class HomeViewTestCase(TestCase):
    """Test case for home view."""

    def test_home_view_status_code(self):
        """Test home view returns 200."""
        c = Client()
        self.assertEqual(c.get('/').status_code, 200)

    def test_home_view_has_anchor(self):
        """Test home view has anchor tag."""
        c = Client()
        self.assertIn(b'</a>', c.get('/').content)


class RegistrationViewTestCase(TestCase):
    """Test case for registration view."""

    def test_register_view_status_code(self):
        """Test register view returns 200."""
        c = Client()
        self.assertEqual(c.get('/register').status_code, 200)

    def test_register_view_has_form(self):
        """Test register view has form."""
        c = Client()
        self.assertIn(b'</form>', c.get('/register').content)


class LoginViewTestCase(TestCase):
    """Test case for login view."""

    def test_register_view_status_code(self):
        """Test login view returns 200."""
        c = Client()
        self.assertEqual(c.get('/login').status_code, 200)

    def test_login_view_has_form(self):
        """Test login view has form."""
        c = Client()
        self.assertIn(b'</form>', c.get('/login').content)
