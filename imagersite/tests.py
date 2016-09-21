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

    def test_home_view_has_register_link(self):
        """Test home view has register link."""
        c = Client()
        self.assertIn(b'href="/accounts/register/"', c.get('/').content)

    def test_home_view_has_login_link(self):
        """Test home view has login link."""
        c = Client()
        self.assertIn(b'href="/accounts/login/"', c.get('/').content)


class RegistrationViewTestCase(TestCase):
    """Test case for registration view."""

    def test_register_view_status_code(self):
        """Test register view returns 200."""
        c = Client()
        self.assertEqual(c.get('/accounts/register/').status_code, 200)

    def test_register_view_has_form(self):
        """Test register view has form."""
        c = Client()
        self.assertIn(b'</form>', c.get('/accounts/register/').content)


class LoginViewTestCase(TestCase):
    """Test case for login view."""

    def test_register_view_status_code(self):
        """Test login view returns 200."""
        c = Client()
        self.assertEqual(c.get('/accounts/login/').status_code, 200)

    def test_login_view_has_form(self):
        """Test login view has form."""
        c = Client()
        self.assertIn(b'</form>', c.get('/accounts/login/').content)
