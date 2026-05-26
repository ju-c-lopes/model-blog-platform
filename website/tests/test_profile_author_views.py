from types import SimpleNamespace

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from website.models.author.AuthorModel import Author
from website.models.user.ReaderModel import Reader
User = get_user_model()


class ProfileAndAuthorViewTests(TestCase):
    def test_create_reader_profile_via_view(self):
        user = User.objects.create_user(
            username="ruser", email="r@test.com", password="p"
        )
        self.client.force_login(user)
        url = reverse("update-profile")
        r = self.client.post(
            url, data={"profile_type": "reader", "name": "Reader Name"}
        )
        self.assertEqual(r.status_code, 302)
        user.refresh_from_db()
        self.assertTrue(hasattr(user, "reader"))

    def test_switch_author_to_reader_via_view(self):
        user = User.objects.create_user(
            username="aruser", email="ar@test.com", password="p"
        )
        Author.objects.create(user=user, author_name="A", author_url_slug="a")
        user.is_staff = True
        user.save()

        self.client.force_login(user)
        url = reverse("update-profile")
        r = self.client.post(url, data={"profile_type": "reader", "name": "Now Reader"})
        self.assertEqual(r.status_code, 302)
        user.refresh_from_db()
        self.assertFalse(hasattr(user, "author"))
        self.assertTrue(hasattr(user, "reader"))

    def test_update_existing_author_name(self):
        user = User.objects.create_user(
            username="upda", email="up@test.com", password="p"
        )
        author = Author.objects.create(
            user=user, author_name="Old Name", author_url_slug="old"
        )
        self.client.force_login(user)
        url = reverse("update-profile")
        r = self.client.post(url, data={"profile_type": "author", "name": "New Name"})
        self.assertEqual(r.status_code, 302)
        author.refresh_from_db()
        self.assertEqual(author.author_name, "New Name")

    def test_edit_author_wrapper_redirects_when_no_author(self):
        from website.views.author.AuthorEditView import edit_author

        user = User.objects.create_user(
            username="noauth", email="n@test.com", password="p"
        )
        req = SimpleNamespace(user=user)
        res = edit_author(req)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res["Location"], "/")

    def test_post_create_requires_author(self):
        user = User.objects.create_user(
            username="pu", email="pu@test.com", password="p"
        )
        self.client.force_login(user)
        url = reverse("create_post")
        r = self.client.get(url)
        self.assertEqual(r.status_code, 302)

    def test_post_create_success_when_author(self):
        user = User.objects.create_user(
            username="postauth", email="pa@test.com", password="p"
        )
        Author.objects.create(user=user, author_name="Poster", author_url_slug="poster")
        self.client.force_login(user)
        url = reverse("create_post")
        data = {
            "title": "T",
            "text": "C",
            "url_slug": "t-unique",
            "meta_description": "md",
        }
        r = self.client.post(url, data=data)
        self.assertEqual(r.status_code, 302)

    def test_reader_edit_helpers(self):
        user = User.objects.create_user(
            username="read", email="r@test.com", password="p"
        )
        Reader.objects.create(user=user)

        class PostDict(dict):
            def getlist(self, k):
                return [self.get(k)] if self.get(k) else []

        req = SimpleNamespace(
            POST=PostDict({"username": user.username, "reader_name": "New Reader"}),
            FILES={},
            user=user,
        )
        from website.views.reader.ReaderEditView import check_request_post as rcp

        rdata = rcp(req)
        self.assertEqual(rdata["username"], user.username)
