from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from website.models.author.AuthorModel import Author

User = get_user_model()

SEO_TEST_SETTINGS = {
    "DEBUG": True,
    "SECURE_SSL_REDIRECT": False,
    "ALLOWED_HOSTS": ["testserver", "localhost", "127.0.0.1"],
}


@override_settings(**SEO_TEST_SETTINGS)
class ViewportDebugTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.author_user = User.objects.create_user(
            email="author@example.com",
            password="pw",
            username="author",
        )
        Author.objects.create(
            user=self.author_user,
            author_name="Author",
            author_url_slug="author",
        )
        self.reader_user = User.objects.create_user(
            email="reader@example.com",
            password="pw",
            username="reader",
        )

    def test_anonymous_does_not_get_viewport_debug(self):
        response = self.client.get(reverse("home"))
        content = response.content.decode()

        self.assertNotIn('id="viewport-debug"', content)
        self.assertNotIn("tela.js", content)

    def test_reader_does_not_get_viewport_debug(self):
        self.client.force_login(self.reader_user)
        response = self.client.get(reverse("home"))
        content = response.content.decode()

        self.assertNotIn('id="viewport-debug"', content)

    def test_author_gets_viewport_debug_widget(self):
        self.client.force_login(self.author_user)
        response = self.client.get(reverse("home"))
        content = response.content.decode()

        self.assertIn('id="viewport-debug"', content)
        self.assertIn("viewport_debug.css", content)
        self.assertIn("tela.js", content)

    def test_author_with_staff_flag_still_gets_viewport_debug(self):
        self.author_user.is_staff = True
        self.author_user.save(update_fields=["is_staff"])
        self.client.force_login(self.author_user)
        response = self.client.get(reverse("home"))
        content = response.content.decode()

        self.assertIn('id="viewport-debug"', content)

    def test_staff_without_author_or_superuser_does_not_get_viewport_debug(self):
        staff_user = User.objects.create_user(
            email="staff@example.com",
            password="pw",
            username="staff-only",
            is_staff=True,
        )
        self.client.force_login(staff_user)
        response = self.client.get(reverse("home"))
        content = response.content.decode()

        self.assertNotIn('id="viewport-debug"', content)

    def test_superuser_gets_viewport_debug_widget(self):
        superuser = User.objects.create_superuser(
            email="admin@example.com",
            password="pw",
            username="admin",
        )
        self.client.force_login(superuser)
        response = self.client.get(reverse("home"))
        content = response.content.decode()

        self.assertIn('id="viewport-debug"', content)
