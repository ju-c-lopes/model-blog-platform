from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.backends.db import SessionStore
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory, TestCase

from website.models.author.AuthorModel import Author
from website.models.post.PostModel import Post
from website.models.user.ReaderModel import Reader
from website.views.post.PostCreateView import edit_post


User = get_user_model()


class ProfileAndPostPermissionTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email="p1@example.com", password="pw", username="p1"
        )
        # create a reader profile initially
        self.reader = Reader.objects.create(
            user=self.user
        )

        # another user and their author+post
        self.other_user = User.objects.create_user(
            email="a1@example.com", password="pw", username="a1"
        )
        self.other_author = Author.objects.create(
            user=self.other_user, author_name="A1", author_url_slug="a1"
        )
        self.post = Post.objects.create(
            author=self.other_author, title="T", text="x", url_slug="u1"
        )

    def test_edit_post_permission_owner_vs_non_owner(self):
        # non-owner tries to edit existing post
        req = self.factory.get("/fake")
        req.user = self.user
        # ensure a session exists for message storage
        req.session = SessionStore()
        req._messages = FallbackStorage(req)
        resp = edit_post(req, url_slug=self.post.url_slug)
        # should be a redirect due to permission denied
        assert resp.status_code in (301, 302)

        # owner can access edit view
        req2 = self.factory.get("/fake")
        req2.user = self.other_user
        # ensure a session exists for message storage
        req2.session = SessionStore()
        req2._messages = FallbackStorage(req2)
        # patch render to avoid template parsing
        import website.views.post.PostCreateView as pcv

        old_render = pcv.render
        pcv.render = lambda *a, **k: type("R", (), {"status_code": 200})()
        try:
            resp2 = edit_post(req2, url_slug=self.post.url_slug)
            assert getattr(resp2, "status_code", None) == 200
        finally:
            pcv.render = old_render
