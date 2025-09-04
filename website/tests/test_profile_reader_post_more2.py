from types import SimpleNamespace

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from website.models.AuthorModel import Author
from website.models.PostModel import Post
from website.models.ReaderModel import Reader

User = get_user_model()


class ProfileReaderPostMore2Test(TestCase):
    def setUp(self):
        self.client = Client()

    def test_update_profile_update_existing_author(self):
        user = User.objects.create_user(
            username="au_existing", email="ae@test.com", password="p"
        )
        Author.objects.create(user=user, author_name="Old", author_url_slug="old")
        self.client.force_login(user)

        url = reverse("update-profile")
        resp = self.client.post(url, {"profile_type": "author", "name": "NewName"})
        self.assertEqual(resp.status_code, 302)
        user.refresh_from_db()
        self.assertEqual(user.author.author_name, "NewName")

    def test_check_reader_form_save_branch(self):
        user = User.objects.create_user(
            username="r_save", email="rs@test.com", password="p"
        )
        reader = Reader.objects.create(user=user, reader_name="OldR")
        post = SimpleNamespace(
            POST={"username": user.username, "reader_name": "NewR"}, FILES={}, user=user
        )
        from website.views.ReaderEditView import check_reader_form

        ok = check_reader_form(post, reader)
        self.assertTrue(ok)
        reader.refresh_from_db()
        self.assertEqual(reader.reader_name, "NewR")

    def test_edit_post_permission_and_owner(self):
        # author A creates post
        ua = User.objects.create_user(
            username="authA", email="a@test.com", password="p"
        )
        author_a = Author.objects.create(user=ua, author_name="A", author_url_slug="a")
        post = Post.objects.create(
            author=author_a,
            title="T",
            url_slug="slug-a",
            meta_description="m",
            text="t",
        )

        # another user B tries to edit -> redirected
        ub = User.objects.create_user(
            username="userB", email="b@test.com", password="p"
        )
        self.client.force_login(ub)
        url = reverse("edit_post", kwargs={"url_slug": post.url_slug})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

        # owner can access
        self.client.force_login(ua)
        resp2 = self.client.get(url)
        self.assertEqual(resp2.status_code, 200)
