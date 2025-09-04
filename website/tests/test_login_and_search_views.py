from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.backends.db import SessionStore
from django.test import RequestFactory, TestCase

from website.models.AuthorModel import Author
from website.models.PostModel import Post
from website.views.LoginView import login_user
from website.views.SearchView import search_posts

User = get_user_model()


class LoginViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def _attach_session_and_messages(self, req):
        req.session = SessionStore()
        req._messages = FallbackStorage(req)

    def test_login_success_redirects(self):
        # create user
        user = User.objects.create_user(
            email="u1@example.com", username="u1", password="pw"
        )
        data = {"email": "u1@example.com", "password": "pw"}
        req = self.factory.post("/login", data)
        self._attach_session_and_messages(req)

        # patch authenticate and check_password to ensure branch
        with (
            patch("website.views.LoginView.authenticate", return_value=user),
            patch("website.views.LoginView.check_password", return_value=True),
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

        with patch("website.views.LoginView.render", fake_render):
            resp = login_user(req)

        assert resp.status_code == 200
        assert getattr(resp, "context", None) is not None
        assert resp.context.get("email_not_found", False) is True


class SearchViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_search_returns_results_and_counts(self):
        user = User.objects.create_user(
            email="a@example.com", username="a", password="pw"
        )
        author = Author.objects.create(
            user=user, author_name="AuthorX", author_url_slug="ax"
        )
        # create matching posts
        Post.objects.create(author=author, title="FindMe", text="abc", url_slug="p1")
        Post.objects.create(
            author=author, title="FindMe two", text="def", url_slug="p2"
        )

        req = self.factory.get("/search", {"query": "FindMe"})

        def fake_render(req_in, template, context=None):
            return SimpleNamespace(status_code=200, context=context)

        with patch("website.views.SearchView.render", fake_render):
            resp = search_posts(req)

        assert resp.status_code == 200
        assert resp.context["results_count"] == 2

    def test_search_page_not_integer_returns_first_page(self):
        user = User.objects.create_user(
            email="b@example.com", username="b", password="pw"
        )
        author = Author.objects.create(
            user=user, author_name="AuthorY", author_url_slug="ay"
        )
        # one matching post
        Post.objects.create(author=author, title="OnlyOne", text="x", url_slug="o1")

        req = self.factory.get("/search", {"query": "OnlyOne", "page": "notint"})

        def fake_render(req_in, template, context=None):
            return SimpleNamespace(status_code=200, context=context)

        with patch("website.views.SearchView.render", fake_render):
            resp = search_posts(req)

        assert resp.status_code == 200
        # posts is a Page object; ensure it corresponds to page 1 by checking object_list length
        assert len(list(resp.context["posts"])) == 1
