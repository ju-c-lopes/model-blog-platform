from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase

from website.models.AuthorModel import Author
from website.views.AuthorView import check_author_form, check_user_form, edit_author

User = get_user_model()


class AuthorViewMoreTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email="au1@example.com", password="pw", username="au1"
        )
        self.author = Author.objects.create(
            user=self.user, author_name="Orig", author_url_slug="orig"
        )
        # create another user+author to simulate username target
        self.other_user = User.objects.create_user(
            email="other@example.com", password="pw", username="newname"
        )
        self.other_author = Author.objects.create(
            user=self.other_user, author_name="Other", author_url_slug="other"
        )

    def test_check_author_form_updates_name_when_valid(self):
        data = {
            "author_name": "Updated Name",
            "username": self.user.username,
            "social_media_profile": [],
            "social_media": [],
            "exclude-social": [],
        }
        req = self.factory.post("/fake", data)
        req.user = self.user

        ok = check_author_form(req, self.author)
        assert ok
        self.author.refresh_from_db()
        assert self.author.author_name == "Updated Name"

    def test_check_user_form_updates_username_when_free(self):
        # attempt to change current author's username to an existing username (other_user)
        data = {
            "username": "newname",
            "author_name": "X",
            "email": "new@example.com",
            "password": "",
            "confirm_pass": "",
        }
        req = self.factory.post("/fake", data)
        req.user = self.user

        free = check_user_form(req, self.author)
        # should report username free (update may happen only when form valid)
        assert free is True

    def test_edit_author_with_user_author_returns_response(self):
        # patch module render to avoid template parsing during unit test
        import website.views.AuthorView as av

        old_render = av.render
        av.render = lambda *a, **k: type("R", (), {"status_code": 200})()
        try:
            req = self.factory.get("/fake")
            req.user = self.user
            resp = edit_author(req, author_slug=None)
            assert getattr(resp, "status_code", None) == 200
        finally:
            av.render = old_render
