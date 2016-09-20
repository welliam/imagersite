from django.test import TestCase, Client


class HomeViewTestCase(TestCase):
    """Test case for home view."""

    def test_home_view_status_code(self):
        """Test home view returns 200."""
        c = Client()
        self.assertEqual(c.get('/').status_code, 200)

    def test_home_view_has_anchor(self):
        """Test home view returns 200."""
        c = Client()
        self.assertIn(b'</a>', c.get('/').content)
