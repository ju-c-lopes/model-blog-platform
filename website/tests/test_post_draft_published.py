from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from website.models.author.AuthorModel import Author
from website.models.post.PostModel import Post
from website.services.post.post_search import search_posts_queryset

User = get_user_model()


class PostDraftPublishedTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.author_user = User.objects.create_user(
            email="author@example.com",
            password="pw",
            username="author",
        )
        self.other_user = User.objects.create_user(
            email="other@example.com",
            password="pw",
            username="other",
        )
        self.staff_user = User.objects.create_user(
            email="staff@example.com",
            password="pw",
            username="staff",
            is_staff=True,
        )
        self.author = Author.objects.create(
            user=self.author_user,
            author_name="Author Name",
            author_url_slug="author-name",
        )
        self.draft_post = Post.objects.create(
            author=self.author,
            title="Rascunho secreto",
            url_slug="rascunho-secreto",
            text="<p>Conteúdo do rascunho.</p>",
            status=Post.DRAFT,
        )
        self.published_post = Post.objects.create(
            author=self.author,
            title="Post publicado",
            url_slug="post-publicado",
            text="<p>Conteúdo publicado.</p>",
            status=Post.PUBLISHED,
            published_date=timezone.now().date(),
        )

    def test_home_lists_only_published_posts(self):
        response = self.client.get(
            reverse("home"),
            secure=True,
        )

        self.assertEqual(response.status_code, 200)
        slugs = [post.url_slug for post in response.context["posts"]]
        self.assertIn(self.published_post.url_slug, slugs)
        self.assertNotIn(self.draft_post.url_slug, slugs)

    def test_search_lists_only_published_posts(self):
        results = search_posts_queryset("")

        self.assertEqual(results.count(), 1)
        self.assertEqual(results.first().url_slug, self.published_post.url_slug)

    def test_anonymous_cannot_view_draft_detail(self):
        response = self.client.get(
            reverse("post_detail", kwargs={"url_slug": self.draft_post.url_slug}),
            secure=True,
        )

        self.assertEqual(response.status_code, 404)

    def test_author_can_view_draft_detail(self):
        self.client.force_login(self.author_user)
        response = self.client.get(
            reverse("post_detail", kwargs={"url_slug": self.draft_post.url_slug}),
            secure=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_draft_preview"])
        self.assertContains(response, "Rascunho")

    def test_staff_can_view_draft_detail(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(
            reverse("post_detail", kwargs={"url_slug": self.draft_post.url_slug}),
            secure=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_draft_preview"])

    def test_other_user_cannot_view_draft_detail(self):
        self.client.force_login(self.other_user)
        response = self.client.get(
            reverse("post_detail", kwargs={"url_slug": self.draft_post.url_slug}),
            secure=True,
        )

        self.assertEqual(response.status_code, 404)

    def test_create_post_as_draft_by_default(self):
        self.client.force_login(self.author_user)
        response = self.client.post(
            reverse("create_post"),
            {
                "title": "Novo rascunho",
                "url_slug": "novo-rascunho",
                "meta_description": "Descrição válida.",
                "text": "<p>Conteúdo do post com mais de dez caracteres.</p>",
                "status": Post.DRAFT,
            },
            secure=True,
        )

        self.assertEqual(response.status_code, 302)
        post = Post.objects.get(url_slug="novo-rascunho")
        self.assertEqual(post.status, Post.DRAFT)

    def test_create_post_as_published(self):
        self.client.force_login(self.author_user)
        response = self.client.post(
            reverse("create_post"),
            {
                "title": "Novo publicado",
                "url_slug": "novo-publicado",
                "meta_description": "Descrição válida.",
                "text": "<p>Conteúdo do post com mais de dez caracteres.</p>",
                "status": Post.PUBLISHED,
            },
            secure=True,
        )

        self.assertEqual(response.status_code, 302)
        post = Post.objects.get(url_slug="novo-publicado")
        self.assertEqual(post.status, Post.PUBLISHED)
        self.assertIsNotNone(post.published_date)

    def test_author_can_publish_draft_from_editor(self):
        self.client.force_login(self.author_user)
        response = self.client.post(
            reverse("edit_post", kwargs={"url_slug": self.draft_post.url_slug}),
            {
                "title": self.draft_post.title,
                "url_slug": self.draft_post.url_slug,
                "meta_description": "",
                "text": self.draft_post.text,
                "status": Post.PUBLISHED,
            },
            secure=True,
        )

        self.assertEqual(response.status_code, 302)
        self.draft_post.refresh_from_db()
        self.assertEqual(self.draft_post.status, Post.PUBLISHED)

        home = self.client.get(
            reverse("home"),
            secure=True,
        )
        slugs = [post.url_slug for post in home.context["posts"]]
        self.assertIn(self.draft_post.url_slug, slugs)

    def test_edit_form_shows_status_field(self):
        self.client.force_login(self.author_user)
        response = self.client.get(
            reverse("edit_post", kwargs={"url_slug": self.draft_post.url_slug}),
            secure=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rascunho")
        self.assertContains(response, "Publicado")
