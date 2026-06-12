from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.backends.db import SessionStore
from django.test import RequestFactory, TestCase
from django.urls import reverse

from website.models.author.AuthorModel import Author
from website.models.post.PostModel import Post
from website.models.post.TagModel import Tag
from website.services.post.post_search import search_posts_queryset
from website.views.post.SearchView import search_posts
from website.views.user.LoginView import login_user

User = get_user_model()


class LoginViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def _attach_session_and_messages(self, req):
        req.session = SessionStore()
        req._messages = FallbackStorage(req)

    def test_login_success_redirects(self):
        # create user
        user = User.objects.create_user(email="u1@example.com", username="u1", password="pw")
        data = {"email": "u1@example.com", "password": "pw"}
        req = self.factory.post("/login", data)
        self._attach_session_and_messages(req)

        # patch authenticate and check_password to ensure branch
        with (
            patch("website.views.user.LoginView.authenticate", return_value=user),
            patch("website.views.user.LoginView.check_password", return_value=True),
        ):
            resp = login_user(req)

        # successful login redirects to '/'
        assert resp.status_code in (301, 302)

    def test_login_email_not_found_renders_with_flag(self):
        data = {"email": "noone@example.com", "password": "pw"}
        req = self.factory.post("/login", data)
        self._attach_session_and_messages(req)

        # patch render to capture context
        def fake_render(req_in, template, context=None, status=200):
            return SimpleNamespace(status_code=status, context=context)

        with patch("website.views.user.LoginView.render", fake_render):
            resp = login_user(req)

        assert resp.status_code == 200
        assert getattr(resp, "context", None) is not None
        assert resp.context.get("email_not_found", False) is True


class SearchViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        user = User.objects.create_user(email="a@example.com", username="a", password="pw")
        self.author = Author.objects.create(user=user, author_name="AuthorX", author_url_slug="ax")

    def _search(self, params):
        req = self.factory.get("/search", params)

        def fake_render(req_in, template, context=None):
            return SimpleNamespace(status_code=200, context=context)

        with patch("website.views.post.SearchView.render", fake_render):
            return search_posts(req)

    def test_search_returns_results_and_counts(self):
        Post.objects.create(author=self.author, title="FindMe", text="abc", url_slug="p1")
        Post.objects.create(author=self.author, title="FindMe two", text="def", url_slug="p2")

        resp = self._search({"query": "FindMe"})

        assert resp.status_code == 200
        assert resp.context["results_count"] == 2
        assert resp.context["is_explore"] is False

    def test_search_page_not_integer_returns_first_page(self):
        Post.objects.create(author=self.author, title="OnlyOne", text="x", url_slug="o1")

        resp = self._search({"query": "OnlyOne", "page": "notint"})

        assert resp.status_code == 200
        assert len(list(resp.context["posts"])) == 1

    def test_search_by_meta_description(self):
        Post.objects.create(
            author=self.author,
            title="Other title",
            text="body",
            meta_description="Guia completo de Docker",
            url_slug="docker-meta",
        )

        resp = self._search({"query": "Docker"})

        assert resp.context["results_count"] == 1
        assert resp.context["posts"][0].url_slug == "docker-meta"

    def test_search_by_tag_name(self):
        tag, _ = Tag.objects.get_or_create(slug="seo", defaults={"name": "SEO"})
        post = Post.objects.create(author=self.author, title="Marketing", text="content", url_slug="seo-post")
        post.tags.add(tag)

        resp = self._search({"query": "SEO"})

        assert resp.context["results_count"] == 1
        assert resp.context["posts"][0].url_slug == "seo-post"

    def test_search_empty_query_lists_all_posts_explore_mode(self):
        Post.objects.create(author=self.author, title="Alpha", text="a", url_slug="alpha")
        Post.objects.create(author=self.author, title="Beta", text="b", url_slug="beta")

        resp = self._search({})

        assert resp.context["is_explore"] is True
        assert resp.context["results_count"] == 2
        assert len(list(resp.context["posts"])) == 2

    def test_search_distinct_does_not_duplicate_post_with_multiple_tags(self):
        tag_python, _ = Tag.objects.get_or_create(slug="python", defaults={"name": "Python"})
        tag_pytest = Tag.objects.create(name="PyTest Search", slug="pytest-search-test")
        post = Post.objects.create(author=self.author, title="Tagged", text="x", url_slug="tagged")
        post.tags.add(tag_python, tag_pytest)

        results = search_posts_queryset("Py")

        assert results.count() == 1
        assert results.first().pk == post.pk

    def test_search_results_post_links_include_return_query(self):
        Post.objects.create(author=self.author, title="FindMe", text="abc", url_slug="p1")

        response = self.client.get(reverse("search_posts"), {"query": "FindMe"})
        content = response.content.decode()

        self.assertIn("from_query=FindMe", content)
