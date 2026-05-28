from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django.urls import reverse

import website.views.reader.ReaderEditView as reader_view
from website.models.user.ReaderModel import Reader

User = get_user_model()


class ReaderEditViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(email="reader@example.com", password="pw", username="reader")
        self.other = User.objects.create_user(email="other@example.com", password="pw", username="other")
        self.reader = Reader.objects.create(user=self.user)

    def test_edit_requires_login(self):
        url = reverse("reader-edit")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response["Location"])

    def test_edit_get_ok_for_reader(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("reader-edit"))
        self.assertEqual(response.status_code, 200)

    def test_edit_redirects_without_reader_profile(self):
        self.client.force_login(self.other)
        response = self.client.get(reverse("reader-edit"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("home"))

    def test_reader_edit_post_success_path(self):
        req = self.factory.post("/", {})
        req.user = self.user

        bundle = MagicMock()
        bundle.user_form.errors = {}
        bundle.reader_form.errors = {}

        with (
            patch.object(reader_view, "get_reader_for_edit", return_value=self.reader),
            patch.object(reader_view, "can_edit", return_value=True),
            patch.object(reader_view, "build_bundle", return_value=bundle),
            patch.object(reader_view, "bundle_is_valid", return_value=True),
            patch.object(reader_view, "save_bundle") as mock_save,
            patch.object(reader_view, "messages"),
            patch.object(reader_view, "redirect", return_value=HttpResponse(status=302)),
        ):
            resp = reader_view.reader_edit(req)
            mock_save.assert_called_once_with(bundle, req)
            self.assertEqual(resp.status_code, 302)

    def test_reader_edit_post_invalid_renders_form(self):
        req = self.factory.post("/", {})
        req.user = self.user

        bundle = MagicMock()
        bundle.user_form.errors = {}
        bundle.reader_form.errors = {}

        with (
            patch.object(reader_view, "get_reader_for_edit", return_value=self.reader),
            patch.object(reader_view, "can_edit", return_value=True),
            patch.object(reader_view, "build_bundle", return_value=bundle),
            patch.object(reader_view, "bundle_is_valid", return_value=False),
            patch.object(reader_view, "add_validation_messages") as mock_msgs,
            patch.object(
                reader_view,
                "as_template_context",
                return_value={"user_form": bundle.user_form},
            ),
            patch.object(reader_view, "render", return_value=HttpResponse(status=200)),
        ):
            resp = reader_view.reader_edit(req)
            mock_msgs.assert_called_once()
            self.assertEqual(resp.status_code, 200)
