from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase

from website.views.author.AuthorEditView import edit_author

User = get_user_model()


class AuthorEditWrapperUnitTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_edit_author_redirects_when_no_slug_and_no_author(self):
        user = User.objects.create_user(email="u2@example.com", password="pw", username="u2")
        req = self.factory.get("/fake")
        req.user = user
        res = edit_author(req, author_slug=None)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res["Location"], "/")
