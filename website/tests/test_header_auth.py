from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from website.models.author.AuthorModel import Author
from website.models.user.ReaderModel import Reader

User = get_user_model()

SEO_TEST_SETTINGS = {
    "DEBUG": True,
    "SECURE_SSL_REDIRECT": False,
    "ALLOWED_HOSTS": ["testserver", "localhost", "127.0.0.1"],
}


@override_settings(**SEO_TEST_SETTINGS)
class HeaderAuthMenuTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse("home")

    def test_guest_sees_login_links(self):
        response = self.client.get(self.home_url)
        content = response.content.decode()

        self.assertIn(reverse("login"), content)
        self.assertIn("Cadastre-se", content)

    def test_superuser_without_profile_sees_admin_menu_not_guest_links(self):
        superuser = User.objects.create_superuser(
            email="admin@example.com",
            password="Admin$Pass1",
            username="admin",
        )
        self.client.force_login(superuser)
        response = self.client.get(self.home_url)
        content = response.content.decode()

        self.assertIn("/admin/", content)
        self.assertIn(reverse("seo_sitemap_dashboard"), content)
        self.assertIn("Django Admin", content)
        self.assertIn("header-login logged", content)
        self.assertNotIn('class="login-link" href="' + reverse("login") + '"', content)

    def test_reader_sees_profile_menu_not_guest_links(self):
        user = User.objects.create_user(
            email="reader@example.com",
            password="Reader$Pass1",
            username="reader-user",
        )
        Reader.objects.create(user=user, reader_name="Reader Name")
        self.client.force_login(user)
        response = self.client.get(self.home_url)
        content = response.content.decode()

        self.assertIn(reverse("reader-edit"), content)
        self.assertIn("Reader Name", content)
        self.assertNotIn('class="login-link" href="' + reverse("login") + '"', content)

    def test_author_sees_create_post_in_menu(self):
        user = User.objects.create_user(
            email="author@example.com",
            password="Author$Pass1",
            username="author-user",
        )
        Author.objects.create(
            user=user,
            author_name="Author Name",
            author_url_slug="author-name",
        )
        self.client.force_login(user)
        response = self.client.get(self.home_url)
        content = response.content.decode()

        self.assertIn(reverse("create_post"), content)
        self.assertIn("Author Name", content)
        self.assertNotIn("Django Admin", content)
        self.assertNotIn(reverse("seo_sitemap_dashboard"), content)

    def test_author_with_staff_flag_but_not_superuser_does_not_see_admin_links(self):
        user = User.objects.create_user(
            email="staff-author@example.com",
            password="Author$Pass1",
            username="staff-author",
            is_staff=True,
        )
        Author.objects.create(
            user=user,
            author_name="Staff Author",
            author_url_slug="staff-author",
        )
        self.client.force_login(user)
        response = self.client.get(self.home_url)
        content = response.content.decode()

        self.assertIn(reverse("create_post"), content)
        self.assertNotIn("Django Admin", content)
        self.assertNotIn(reverse("seo_sitemap_dashboard"), content)

    def test_superuser_author_sees_admin_link_in_profile_menu(self):
        superuser = User.objects.create_superuser(
            email="author-admin@example.com",
            password="Admin$Pass1",
            username="author-admin",
        )
        Author.objects.create(
            user=superuser,
            author_name="Admin Author",
            author_url_slug="admin-author",
        )
        self.client.force_login(superuser)
        response = self.client.get(self.home_url)
        content = response.content.decode()

        self.assertIn(reverse("create_post"), content)
        self.assertIn("/admin/", content)
        self.assertIn("Django Admin", content)
        self.assertIn(reverse("seo_sitemap_dashboard"), content)
        self.assertNotIn('class="login-link" href="' + reverse("login") + '"', content)
