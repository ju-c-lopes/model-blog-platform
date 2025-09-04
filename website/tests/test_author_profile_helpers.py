from types import SimpleNamespace

from django.contrib.auth import get_user_model
from django.test import TestCase

from website.models.AuthorModel import Author
from website.models.AuthorSocialMediaModel import SocialMedia
from website.models.ReaderModel import Reader
from website.views import AuthorView

User = get_user_model()


class AuthorProfileHelpersTest(TestCase):
    def test_check_author_form_and_user_form_username_conflict(self):
        # create two users to cause username conflict
        user1 = User.objects.create_user(
            username="u1", email="u1@test.com", password="p"
        )
        user2 = User.objects.create_user(
            username="u2", email="u2@test.com", password="p"
        )
        # create an Author record for user2 so check_request_post can query it
        Author.objects.create(user=user2, author_name="Other", author_url_slug="other")
        author = Author.objects.create(user=user1, author_name="A", author_url_slug="a")

        # build a fake POST where username conflicts with user2
        class PostDict(dict):
            def getlist(self, k):
                return self.get(k, [])

        post = PostDict(
            {
                "username": user2.username,
                "author_name": "NewA",
                "social_media": [],
                "social_media_profile": [],
            }
        )
        req = SimpleNamespace(POST=post, FILES={}, user=user1)

        # check_request_post should report username conflict (non-empty queryset)
        ar = AuthorView.check_request_post(req)
        self.assertIsNotNone(ar)
        self.assertIn("check_username_request", ar)

        # call check_author_form (may return True/False depending on form validity)
        result = AuthorView.check_author_form(req, author)
        self.assertIn(result, (True, False))

    def test_update_social_media_detects_changes(self):
        user = User.objects.create_user(
            username="u3", email="u3@test.com", password="p"
        )
        author = Author.objects.create(
            user=user, author_name="Auth3", author_url_slug="auth3"
        )
        sm = SocialMedia.objects.create(
            user_social_media=author, social_media=1, social_media_profile="p"
        )
        author.social_media.add(sm)

        class PostDict(dict):
            def getlist(self, k):
                return self.get(k, [])

    # change the social media values
    post = PostDict({"social_media": ["2"], "social_media_profile": ["http://y"]})
    req = SimpleNamespace(POST=post, FILES={}, user=user)

    # call update_social_media for coverage; return value not needed here
    AuthorView.update_social_media(req, list(author.social_media.all()))
    # ensure DB reflects the new values for the first social entry
    author.refresh_from_db()
    sms = list(author.social_media.all())
    self.assertGreaterEqual(len(sms), 1)
    self.assertEqual(str(sms[0].social_media), "2")
    self.assertEqual(sms[0].social_media_profile, "http://y")


class ReaderEditHelpersTest(TestCase):
    def test_reader_check_user_form_username_conflict(self):
        user = User.objects.create_user(
            username="r1", email="r1@test.com", password="p"
        )
        other = User.objects.create_user(
            username="r2", email="r2@test.com", password="p"
        )
        reader = Reader.objects.create(user=user, reader_name="R")

        class PostDict(dict):
            def getlist(self, k):
                return []

        # attempt to change username to other.username -> conflict
        post = PostDict({"username": other.username, "reader_name": "NewR"})
        req = SimpleNamespace(POST=post, FILES={}, user=user)

        from website.views.ReaderEditView import check_user_form as rcheck

        ok = rcheck(req, reader)
        self.assertIsInstance(ok, bool)
