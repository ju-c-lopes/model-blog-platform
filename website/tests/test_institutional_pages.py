from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from website.models.author.AuthorModel import Author
from website.models.post.PostModel import Post

User = get_user_model()

SEO_TEST_SETTINGS = {
    "DEBUG": True,
    "SECURE_SSL_REDIRECT": False,
    "ALLOWED_HOSTS": ["testserver", "localhost", "127.0.0.1"],
}


@override_settings(**SEO_TEST_SETTINGS)
class InstitutionalPagesTests(TestCase):
    def setUp(self):
        self.client = Client()
        user = User.objects.create_user(email="author@example.com", password="pw", username="author")
        self.author = Author.objects.create(
            user=user,
            author_name="Author Name",
            author_url_slug="author-name",
        )
        self.post = Post.objects.create(
            author=self.author,
            title="Post Publicado",
            url_slug="post-publicado",
            text="<p>Conteúdo.</p>",
            status=Post.PUBLISHED,
        )

    def test_institutional_pages_return_200(self):
        routes = ("about", "contact", "privacy", "cookies", "html_sitemap")
        for route_name in routes:
            with self.subTest(route=route_name):
                response = self.client.get(reverse(route_name))
                self.assertEqual(response.status_code, 200)

    def test_legal_pages_are_indexable(self):
        for route_name in ("privacy", "cookies", "about", "contact", "html_sitemap"):
            with self.subTest(route=route_name):
                response = self.client.get(reverse(route_name))
                content = response.content.decode()
                self.assertNotIn('content="noindex', content)

    def test_html_sitemap_lists_published_content(self):
        response = self.client.get(reverse("html_sitemap"))
        content = response.content.decode()

        self.assertIn("/post/post-publicado/", content)
        self.assertIn("Post Publicado", content)
        self.assertIn("Author Name", content)
        self.assertIn("Em breve", content)

    def test_html_sitemap_institutional_section(self):
        response = self.client.get(reverse("html_sitemap"))
        content = response.content.decode()

        self.assertIn(reverse("about"), content)
        self.assertIn(reverse("contact"), content)
        self.assertIn(reverse("privacy"), content)
        self.assertIn(reverse("cookies"), content)

    def test_institutional_routes_in_xml_sitemap(self):
        response = self.client.get(reverse("sitemap"))
        content = response.content.decode()

        for route_name in ("about", "contact", "privacy", "cookies", "html_sitemap"):
            with self.subTest(route=route_name):
                self.assertIn(reverse(route_name), content)

    def test_base_includes_cookie_banner(self):
        response = self.client.get(reverse("home"))
        content = response.content.decode()

        self.assertIn('id="cookie-notice-banner"', content)
        self.assertIn("Entendi", content)
        self.assertIn(reverse("cookies"), content)

    def test_footer_links_to_institutional_pages(self):
        response = self.client.get(reverse("home"))
        content = response.content.decode()

        self.assertIn(reverse("about"), content)
        self.assertIn(reverse("contact"), content)
        self.assertIn(reverse("privacy"), content)
        self.assertIn(reverse("cookies"), content)
        self.assertIn(reverse("html_sitemap"), content)

    def test_header_links_sobre_and_contato(self):
        response = self.client.get(reverse("home"))
        content = response.content.decode()

        self.assertIn(f'href="{reverse("about")}"', content)
        self.assertIn(f'href="{reverse("contact")}"', content)
