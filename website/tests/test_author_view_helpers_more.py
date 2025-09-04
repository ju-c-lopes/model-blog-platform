from types import SimpleNamespace

from django.contrib.auth import get_user_model
from django.test import TestCase

from website.models.AuthorModel import Author
from website.models.AuthorSocialMediaModel import SocialMedia
from website.views.AuthorView import (
    check_request_post,
    create_social_media,
    exclude_social_media,
    update_social_media,
)

User = get_user_model()


class PostDict(dict):
    def getlist(self, k):
        return self.get(k, [])


class AuthorViewHelpersMoreTest(TestCase):
    def test_check_request_post_detects_new_social_addition(self):
        user = User.objects.create_user(
            username="au1", email="au1@test.com", password="p"
        )
        author = Author.objects.create(
            user=user, author_name="Au1", author_url_slug="au1"
        )
        # author has zero social entries

        post = PostDict(
            {
                "username": user.username,
                "author_name": "Au1",
                "social_media": ["1", "2"],
                "social_media_profile": ["http://a", "http://b"],
                "exclude-social": [],
            }
        )
        req = SimpleNamespace(POST=post, FILES={}, user=user)

        res = check_request_post(req)
        self.assertIsNotNone(res)
        # new_social_addition should be True because POST has 2 profiles while author has 0
        self.assertTrue(res.get("new_social_addition"))

    def test_update_social_media_updates_existing_entries(self):
        user = User.objects.create_user(
            username="au2", email="au2@test.com", password="p"
        )
        author = Author.objects.create(
            user=user, author_name="Au2", author_url_slug="au2"
        )
        sm = SocialMedia.objects.create(
            user_social_media=author, social_media=1, social_media_profile="old"
        )
        author.social_media.add(sm)

        post = PostDict({"social_media": ["2"], "social_media_profile": ["new"]})
        req = SimpleNamespace(POST=post, FILES={}, user=user)

        changed = update_social_media(req, list(author.social_media.all()))
        self.assertTrue(changed)
        author.refresh_from_db()
        sms = list(author.social_media.all())
        self.assertEqual(str(sms[0].social_media), "2")
        self.assertEqual(sms[0].social_media_profile, "new")

    def test_create_social_media_appends_new_entries(self):
        user = User.objects.create_user(
            username="au3", email="au3@test.com", password="p"
        )
        author = Author.objects.create(
            user=user, author_name="Au3", author_url_slug="au3"
        )
        sm = SocialMedia.objects.create(
            user_social_media=author, social_media=1, social_media_profile="p"
        )
        author.social_media.add(sm)

        # POST contains two entries; create_social_media should add the extra one
        post = PostDict(
            {
                "social_media": ["1", "2"],
                "social_media_profile": ["p", "http://x"],
                "username": user.username,
            }
        )
        req = SimpleNamespace(POST=post, FILES={}, user=user)
        author_request_post = {"username": user.username}

        create_social_media(req, author_request_post)
        author.refresh_from_db()
        self.assertEqual(author.social_media.count(), 2)

    def test_exclude_social_media_removes_entries(self):
        user = User.objects.create_user(
            username="au4", email="au4@test.com", password="p"
        )
        author = Author.objects.create(
            user=user, author_name="Au4", author_url_slug="au4"
        )
        sm1 = SocialMedia.objects.create(
            user_social_media=author, social_media=1, social_media_profile="p1"
        )
        sm2 = SocialMedia.objects.create(
            user_social_media=author, social_media=2, social_media_profile="p2"
        )
        author.social_media.add(sm1)
        author.social_media.add(sm2)

        post = PostDict(
            {
                "username": user.username,
                "author_name": "Au4",
                "social_media": ["1", "2"],
                "social_media_profile": ["p1", "p2"],
                "exclude-social": ["2"],
            }
        )
        req = SimpleNamespace(POST=post, FILES={}, user=user)

        # exclude_social_media uses check_request_post internally, but here we call directly
        exclude_social_media(req, author)
        author.refresh_from_db()
        # only one remaining
        self.assertEqual(author.social_media.count(), 1)
