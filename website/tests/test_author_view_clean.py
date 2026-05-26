from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from unittest.mock import patch

import website.views.author.AuthorView as av
from website.models.author.AuthorModel import Author

User = get_user_model()


class AuthorViewCleanTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.owner = User.objects.create_user(
            email="owner@example.com", password="pw", username="owner"
        )
        self.other = User.objects.create_user(
            email="other@example.com", password="pw", username="other"
        )
        self.author = Author.objects.create(
            user=self.owner, author_name="Owner", author_url_slug="owner"
        )

    def test_view_author_page_owner_and_non_owner(self):
        captured = {}

        def fake_render(request, template_name=None, context=None, status=200):
            resp = HttpResponse(status=status)
            resp.context = context or {}
            captured["ctx"] = context or {}
            return resp

        with patch.object(av, "render", side_effect=fake_render):
            req = self.factory.get("/")
            req.user = self.other
            resp = av.view_author_page(req, slug=self.author.author_url_slug)
            self.assertEqual(resp.status_code, 200)
            self.assertFalse(captured["ctx"]["author_connected"])

            req2 = self.factory.get("/")
            req2.user = self.owner
            resp2 = av.view_author_page(req2, slug=self.author.author_url_slug)
            self.assertEqual(resp2.status_code, 200)
            self.assertTrue(captured["ctx"]["author_connected"])
