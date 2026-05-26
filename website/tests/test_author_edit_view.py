from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django.urls import reverse

import website.views.author.AuthorEditView as edit_view
from website.models.author.AuthorModel import Author

User = get_user_model()


class AuthorEditViewTests(TestCase):
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

    def test_edit_requires_login(self):
        url = reverse("edit_author", kwargs={"slug": self.author.author_url_slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response["Location"])

    def test_edit_forbidden_for_non_owner(self):
        self.client.force_login(self.other)
        url = reverse("edit_author", kwargs={"slug": self.author.author_url_slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["Location"],
            reverse("author", kwargs={"slug": self.author.author_url_slug}),
        )

    def test_edit_get_ok_for_owner(self):
        self.client.force_login(self.owner)
        url = reverse("edit_author", kwargs={"slug": self.author.author_url_slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_edit_author_profile_post_success_path(self):
        req = self.factory.post("/", {})
        req.user = self.owner

        bundle = MagicMock()
        bundle.user_form.errors = {}

        with (
            patch.object(edit_view, "get_author_for_edit", return_value=self.author),
            patch.object(edit_view, "can_edit", return_value=True),
            patch.object(edit_view, "build_bundle", return_value=bundle),
            patch.object(edit_view, "bundle_is_valid", return_value=True),
            patch.object(edit_view, "save_bundle") as mock_save,
            patch.object(edit_view, "messages"),
            patch.object(edit_view, "redirect", return_value=HttpResponse(status=302)),
        ):
            resp = edit_view.edit_author_profile(
                req, slug=self.author.author_url_slug
            )
            mock_save.assert_called_once_with(bundle, req)
            self.assertEqual(resp.status_code, 302)

    def test_edit_author_profile_post_invalid_renders_form(self):
        req = self.factory.post("/", {})
        req.user = self.owner

        bundle = MagicMock()
        bundle.user_form.errors = {}

        with (
            patch.object(edit_view, "get_author_for_edit", return_value=self.author),
            patch.object(edit_view, "can_edit", return_value=True),
            patch.object(edit_view, "build_bundle", return_value=bundle),
            patch.object(edit_view, "bundle_is_valid", return_value=False),
            patch.object(edit_view, "add_validation_messages") as mock_msgs,
            patch.object(
                edit_view,
                "as_template_context",
                return_value={"user_form": bundle.user_form},
            ),
            patch.object(edit_view, "render", return_value=HttpResponse(status=200)),
        ):
            resp = edit_view.edit_author_profile(
                req, slug=self.author.author_url_slug
            )
            mock_msgs.assert_called_once()
            self.assertEqual(resp.status_code, 200)

    def test_edit_author_redirects_when_no_author_profile(self):
        user = User.objects.create_user(
            email="noauth@example.com", password="pw", username="noauth"
        )
        req = self.factory.get("/")
        req.user = user
        resp = edit_view.edit_author(req, author_slug=None)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp["Location"], "/")

    def test_edit_author_delegates_with_author_slug(self):
        req = self.factory.get("/")
        req.user = self.owner

        with patch.object(
            edit_view, "edit_author_profile", return_value=HttpResponse(status=200)
        ) as mock_edit:
            edit_view.edit_author(req, author_slug="owner")
            mock_edit.assert_called_once_with(req, "owner")
