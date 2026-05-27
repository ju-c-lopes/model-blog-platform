from types import SimpleNamespace

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from website.models.author.AuthorModel import Author
from website.models.post.PostModel import Post
from website.models.user.ReaderModel import Reader

User = get_user_model()


class ProfileReaderPostViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_update_profile_create_author_from_reader(self):
        user = User.objects.create_user(
            username="p1", email="p1@test.com", password="p"
        )
        self.client.force_login(user)

        url = reverse("update-profile")
        data = {"profile_type": "author", "name": "New Author"}
        resp = self.client.post(url, data)
        # redirect on success
        self.assertEqual(resp.status_code, 302)
        user.refresh_from_db()
        self.assertTrue(hasattr(user, "author"))

    def test_update_profile_create_reader_from_none(self):
        user = User.objects.create_user(
            username="p2", email="p2@test.com", password="p"
        )
        self.client.force_login(user)

        url = reverse("update-profile")
        data = {"profile_type": "reader", "name": "New Reader"}
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 302)
        user.refresh_from_db()
        self.assertTrue(hasattr(user, "reader"))

    def test_reader_edit_get_for_logged_in_reader(self):
        user = User.objects.create_user(
            username="r1", email="r1@test.com", password="p"
        )
        Reader.objects.create(user=user)
        self.client.force_login(user)
        response = self.client.get(reverse("reader-edit"))
        self.assertEqual(response.status_code, 200)

    def test_post_create_requires_author_profile(self):
        user = User.objects.create_user(
            username="pp1", email="pp1@test.com", password="p"
        )
        self.client.force_login(user)

        url = reverse("create_post")
        resp = self.client.get(url)
        # should redirect because no author profile
        self.assertEqual(resp.status_code, 302)

    def test_post_create_success_with_author(self):
        user = User.objects.create_user(
            username="pp2", email="pp2@test.com", password="p"
        )
        # ensure an author profile exists for this user
        Author.objects.create(user=user, author_name="AuthX", author_url_slug="authx")
        self.client.force_login(user)

        url = reverse("create_post")
        data = {
            "title": "T",
            "url_slug": "t",
            "meta_description": "m",
            "text": "content",
        }
        resp = self.client.post(url, data)
        # should redirect to post detail on success
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Post.objects.filter(url_slug="t").exists())
