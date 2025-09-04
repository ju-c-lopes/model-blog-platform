from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from website.models.AuthorModel import Author
from website.models.PostModel import Post

User = get_user_model()


class ReactionToggleTests(TestCase):
    def setUp(self):
        # create user and author
        self.user = User.objects.create_user(
            username="tester", email="t@test.com", password="pass"
        )
        self.author_user = User.objects.create_user(
            username="author", email="a@test.com", password="pass"
        )
        self.author = Author.objects.create(user=self.author_user, author_name="Author")
        self.post = Post.objects.create(
            author=self.author, title="T", url_slug="t-slug", text="body"
        )

    def test_like_then_switch_to_love_decrements_like_counter(self):
        self.client.force_login(self.user)

        # initial counts
        self.assertEqual(self.post.likes.count(), 0)
        self.assertEqual(self.post.loves.count(), 0)

        # like the post
        url_like = reverse("post_toggle_like", kwargs={"url_slug": self.post.url_slug})
        r1 = self.client.post(url_like)
        self.post.refresh_from_db()
        self.assertEqual(r1.status_code, 200)
        data1 = r1.json()
        self.assertTrue(data1.get("liked"))
        self.assertEqual(data1.get("likes_count"), 1)
        self.assertEqual(self.post.likes.count(), 1)
        self.assertEqual(self.post.loves.count(), 0)

        # now switch to love
        url_love = reverse("post_toggle_love", kwargs={"url_slug": self.post.url_slug})
        r2 = self.client.post(url_love)
        self.post.refresh_from_db()
        self.assertEqual(r2.status_code, 200)
        data2 = r2.json()
        self.assertTrue(data2.get("loved"))
        self.assertEqual(data2.get("loves_count"), 1)
        self.assertEqual(data2.get("likes_count"), 0)
        self.assertEqual(self.post.likes.count(), 0)
        self.assertEqual(self.post.loves.count(), 1)

    def test_undo_like_removes_relation_and_decrements(self):
        self.client.force_login(self.user)
        url_like = reverse("post_toggle_like", kwargs={"url_slug": self.post.url_slug})

        # like
        r1 = self.client.post(url_like)
        self.post.refresh_from_db()
        self.assertEqual(r1.status_code, 200)
        self.assertEqual(self.post.likes.count(), 1)

        # unlike (toggle)
        r2 = self.client.post(url_like)
        self.post.refresh_from_db()
        self.assertEqual(r2.status_code, 200)
        data2 = r2.json()
        self.assertFalse(data2.get("liked"))
        self.assertEqual(data2.get("likes_count"), 0)
        self.assertEqual(self.post.likes.count(), 0)

    def test_multiple_users_counts_and_switching(self):
        user2 = User.objects.create_user(
            username="tester2", email="t2@test.com", password="pass"
        )
        url_like = reverse("post_toggle_like", kwargs={"url_slug": self.post.url_slug})
        url_love = reverse("post_toggle_love", kwargs={"url_slug": self.post.url_slug})
        # user1 likes
        self.client.force_login(self.user)
        self.client.post(url_like)
        self.post.refresh_from_db()
        self.assertEqual(self.post.likes.count(), 1)

        # user2 likes
        self.client.force_login(user2)
        self.client.post(url_like)
        self.post.refresh_from_db()
        self.assertEqual(self.post.likes.count(), 2)

        # user1 switches to love
        self.client.force_login(self.user)
        r3 = self.client.post(url_love)
        self.post.refresh_from_db()
        self.assertEqual(r3.status_code, 200)
        data3 = r3.json()
        self.assertEqual(data3.get("likes_count"), 1)
        self.assertEqual(data3.get("loves_count"), 1)
        self.assertEqual(self.post.likes.count(), 1)
        self.assertEqual(self.post.loves.count(), 1)

    def test_guest_cannot_toggle_reaction(self):
        self.client.logout()
        url_like = reverse("post_toggle_like", kwargs={"url_slug": self.post.url_slug})
        r = self.client.post(url_like)
        self.assertEqual(r.status_code, 403)
