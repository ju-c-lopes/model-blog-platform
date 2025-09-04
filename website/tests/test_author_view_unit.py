from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase

from website.models.AuthorModel import Author
from website.models.AuthorSocialMediaModel import SocialMedia
from website.views.AuthorView import (
    check_request_post,
    create_social_media,
    edit_author,
    exclude_social_media,
    update_social_media,
)

User = get_user_model()


class AuthorViewUnitTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # create a user and author
        self.user = User.objects.create_user(
            email="u1@example.com", password="pw", username="u1"
        )
        self.author = Author.objects.create(
            user=self.user, author_name="A1", author_url_slug="a1"
        )

    def test_check_request_post_none_on_get(self):
        req = self.factory.get("/fake")
        req.user = self.user
        self.assertIsNone(check_request_post(req))

    def test_check_request_post_with_post_lists(self):
        # ensure author has no social media
        self.author.social_media.clear()
        data = {
            "username": self.user.username,
            "author_name": "New Name",
            "social_media_profile": ["p1", "p2"],
            "exclude-social": [""],
            "social_media": ["1", "2"],
        }
        req = self.factory.post("/fake", data)
        req.user = self.user
        # call should return a dict with keys
        d = check_request_post(req)
        assert d["username"] == self.user.username
        assert isinstance(d["new_social_addition"], bool)

    def test_update_create_exclude_social_media_flow(self):
        # create one existing social media
        s1 = SocialMedia.objects.create(
            user_social_media=self.author, social_media=1, social_media_profile="pold"
        )
        self.author.social_media.add(s1)

        # prepare post with updated values and an extra new one
        data = {
            "social_media": ["1", "2"],
            "social_media_profile": ["pnew", "pnew2"],
            "exclude-social": [""],
            "username": self.user.username,
            "author_name": "New",
        }
        req = self.factory.post("/fake", data)
        req.user = self.user

        # update_social_media should update existing entry and return True
        updated = update_social_media(req, list(self.author.social_media.all()))
        assert updated
        s1.refresh_from_db()
        assert s1.social_media_profile == "pnew"

        # create_social_media should add a new SocialMedia for the author
        author_request_post = {"username": self.user.username}
        create_social_media(req, author_request_post)
        assert self.author.social_media.count() >= 2

        # now test exclude_social_media: mark first social to exclude
        exclude_id = str(s1.social_media)
        req2 = self.factory.post(
            "/fake",
            {
                "exclude-social": [exclude_id],
                "username": self.user.username,
                "author_name": self.author.author_name,
            },
        )
        req2.user = self.user
        exclude_social_media(req2, self.author)
        # ensure deletion occurred (s1 should be deleted)
        from django.core.exceptions import ObjectDoesNotExist

        try:
            s1.refresh_from_db()
            still = True
        except ObjectDoesNotExist:
            still = False
        assert not still

    def test_edit_author_redirects_when_no_slug_and_no_author(self):
        # request.user without author attr
        anon = User.objects.create_user(
            email="u2@example.com", password="pw", username="u2"
        )
        req = self.factory.get("/fake")
        req.user = anon
        res = edit_author(req, author_slug=None)
        # should be an HttpResponseRedirect to '/'
        assert res.status_code in (301, 302)
