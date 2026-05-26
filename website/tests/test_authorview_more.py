from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from unittest.mock import patch

from website.models.author.AuthorModel import Author
from website.views.author.AuthorEditView import edit_author

User = get_user_model()


class AuthorEditWrapperTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email="au1@example.com", password="pw", username="au1"
        )
        self.author = Author.objects.create(
            user=self.user, author_name="Orig", author_url_slug="orig"
        )

    def test_edit_author_with_user_author_returns_response(self):
        with patch(
            "website.views.author.AuthorEditView.edit_author_profile",
            return_value=HttpResponse(status=200),
        ):
            req = self.factory.get("/fake")
            req.user = self.user
            resp = edit_author(req, author_slug=None)
            self.assertEqual(resp.status_code, 200)
