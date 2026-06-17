from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from website.models.author.AuthorModel import Author
from website.models.post.PostModel import Post
from website.models.seo.SitemapEntryModel import SitemapEntry, SitemapHealthCheck
from website.services.seo.sitemap_builder import collect_sitemap_urls, normalize_path
from website.services.seo.sitemap_health import check_sitemap_urls

User = get_user_model()


class SitemapXmlTests(TestCase):
    def setUp(self):
        self.client = Client()
        user = User.objects.create_user(email="author@example.com", password="pw", username="author")
        self.author = Author.objects.create(
            user=user,
            author_name="Author Name",
            author_url_slug="author-name",
        )
        self.published = Post.objects.create(
            author=self.author,
            title="Publicado",
            url_slug="post-publicado",
            text="<p>Conteúdo publicado.</p>",
            status=Post.PUBLISHED,
        )
        self.draft = Post.objects.create(
            author=self.author,
            title="Rascunho",
            url_slug="post-rascunho",
            text="<p>Conteúdo rascunho.</p>",
            status=Post.DRAFT,
        )

    def test_sitemap_contains_published_post_not_draft(self):
        response = self.client.get(reverse("sitemap"))

        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn("/post/post-publicado/", content)
        self.assertNotIn("/post/post-rascunho/", content)

    def test_sitemap_lastmod_reflects_post_updated_date(self):
        updated = timezone.now() - timedelta(days=2)
        Post.objects.filter(pk=self.published.pk).update(updated_date=updated)
        self.published.refresh_from_db()

        response = self.client.get(reverse("sitemap"))
        content = response.content.decode()

        self.assertIn(self.published.updated_date.strftime("%Y-%m-%d"), content)

    def test_exclude_override_removes_url_from_sitemap(self):
        post_path = normalize_path(reverse("post_detail", kwargs={"url_slug": self.published.url_slug}))
        SitemapEntry.objects.create(path=post_path, entry_type=SitemapEntry.EXCLUDE)

        response = self.client.get(reverse("sitemap"))
        content = response.content.decode()

        self.assertNotIn("/post/post-publicado/", content)

    def test_include_override_adds_manual_url(self):
        manual_path = "/pagina-manual-seo/"
        SitemapEntry.objects.create(
            path=manual_path,
            entry_type=SitemapEntry.INCLUDE,
            lastmod=timezone.now(),
        )

        response = self.client.get(reverse("sitemap"))
        content = response.content.decode()

        self.assertIn(manual_path, content)
        urls = collect_sitemap_urls()
        self.assertTrue(any(item.path == manual_path for item in urls))


class RobotsTxtTests(TestCase):
    def test_robots_txt_disallows_admin_and_references_sitemap(self):
        response = self.client.get(reverse("robots"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain")
        content = response.content.decode()
        self.assertIn("Disallow: /admin/", content)
        self.assertIn("Disallow: /nossa-equipe/*/edit", content)
        self.assertNotIn("Disallow: /login/", content)
        self.assertNotIn("Disallow: /cadastre-se/", content)
        disallow_lines = [line for line in content.splitlines() if line.startswith("Disallow:")]
        self.assertNotIn("Disallow: /nossa-equipe/", disallow_lines)
        self.assertIn("Sitemap:", content)
        self.assertIn("/sitemap.xml", content)

    def test_robots_txt_catch_all_block_is_last_before_sitemap(self):
        from website.services.seo.robots_txt import ROBOTS_RULES, build_robots_txt_body

        self.assertEqual(ROBOTS_RULES[-1]["user_agent"], "*")
        body = build_robots_txt_body("https://example.com/sitemap.xml")
        self.assertTrue(body.strip().endswith("Sitemap: https://example.com/sitemap.xml"))


class SitemapDashboardTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create_superuser(
            email="admin@example.com",
            password="pw",
            username="admin",
        )
        self.user = User.objects.create_user(
            email="user@example.com",
            password="pw",
            username="user",
        )
        self.url = reverse("seo_sitemap_dashboard")

    def test_anonymous_redirects_to_login(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_regular_user_gets_forbidden(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)

    def test_superuser_can_access_dashboard(self):
        self.client.force_login(self.superuser)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Painel de manutenção do sitemap")

    def test_superuser_can_exclude_url_via_form(self):
        user = User.objects.create_user(email="a@example.com", password="pw", username="a")
        author = Author.objects.create(user=user, author_name="A", author_url_slug="a")
        post = Post.objects.create(
            author=author,
            title="T",
            url_slug="excluir-sitemap",
            text="<p>Conteúdo.</p>",
            status=Post.PUBLISHED,
        )
        post_path = normalize_path(reverse("post_detail", kwargs={"url_slug": post.url_slug}))

        self.client.force_login(self.superuser)
        response = self.client.post(
            self.url,
            {"action": "exclude", "path": post_path, "notes": "teste"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(SitemapEntry.objects.filter(path=post_path, entry_type=SitemapEntry.EXCLUDE).exists())

    def test_verify_action_persists_health_checks(self):
        self.client.force_login(self.superuser)
        response = self.client.post(self.url, {"action": "verify"}, HTTP_HOST="example.com")

        self.assertEqual(response.status_code, 302)
        health = SitemapHealthCheck.objects.get(path=normalize_path(reverse("home")))
        self.assertEqual(health.status_code, 200)

    def test_health_check_reports_200_for_home(self):
        results = check_sitemap_urls(
            [item for item in collect_sitemap_urls() if item.path == normalize_path(reverse("home"))],
            http_host="example.com",
        )

        self.assertEqual(results[normalize_path(reverse("home"))], 200)
