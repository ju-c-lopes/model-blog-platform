from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from website.models.AuthorModel import Author
from website.models.AuthorSocialMediaModel import SocialMedia
from website.views import AuthorView

User = get_user_model()


class AuthorHelpersTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="auth", email="auth@test.com", password="pass"
        )
        self.author = Author.objects.create(user=self.user, author_name="Auth")
        # add one social
        SocialMedia.objects.create(
            user_social_media=self.author,
            social_media=1,
            social_media_profile="http://x",
        )

    def test_check_request_post_returns_expected_structure(self):
        # simulate request with POST and FILES
        class DummyReq:
            class POST_DICT(dict):
                from django.contrib.auth import get_user_model
                from django.test import TestCase
                from django.urls import reverse

                from website.models.AuthorModel import Author
                from website.models.AuthorSocialMediaModel import SocialMedia
                from website.views import AuthorView

                User = get_user_model()

                class AuthorHelpersTests(TestCase):
                    def setUp(self):
                        self.user = User.objects.create_user(
                            username="auth", email="auth@test.com", password="pass"
                        )
                        self.author = Author.objects.create(
                            user=self.user, author_name="Auth"
                        )
                        # add one social
                        SocialMedia.objects.create(
                            user_social_media=self.author,
                            social_media=1,
                            social_media_profile="http://x",
                        )

                    def test_check_request_post_returns_expected_structure(self):
                        # simulate request with POST and FILES
                        class DummyReq:
                            class POST_DICT(dict):
                                def getlist(self, k):
                                    return self.get(k, [])

                            POST = POST_DICT(
                                {
                                    "username": self.user.username,
                                    "author_name": "A",
                                    "social_media": ["1"],
                                    "social_media_profile": ["u"],
                                    "exclude-social": [""],
                                }
                            )
                            FILES = {}
                            user = self.user

                        data = AuthorView.check_request_post(DummyReq)
                        self.assertIn("username", data)
                        self.assertIn("new_social_addition", data)

                    def test_update_social_media_detects_changes(self):
                        class DummyReq:
                            class POST_DICT(dict):
                                def getlist(self, k):
                                    return self.get(k, [])

                            POST = POST_DICT(
                                {
                                    "social_media": ["2"],
                                    "social_media_profile": ["http://y"],
                                }
                            )
                            user = self.user

                        # existing social is different -> should mark updated
                        updated = AuthorView.update_social_media(
                            DummyReq, list(self.author.social_media.all())
                        )
                        self.assertTrue(updated)

                class ProfileUpdateTests(TestCase):
                    def setUp(self):
                        self.user = User.objects.create_user(
                            username="u", email="u@test.com", password="p"
                        )

                    def test_create_author_profile_via_view(self):
                        self.client.force_login(self.user)
                        url = reverse("update-profile")
                        # post to create author
                        r = self.client.post(
                            url, data={"profile_type": "author", "name": "New Author"}
                        )
                        self.assertEqual(r.status_code, 302)
                        self.user.refresh_from_db()
                        self.assertTrue(hasattr(self.user, "author"))
