from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from website.models.AuthorModel import Author
from website.models.PostModel import Post
from website.models.ReaderModel import Reader

User = get_user_model()


class ViewSmokeTests(TestCase):
    def setUp(self):
        # create an author user and reader user
        self.author_user = User.objects.create_user(
            username="author", email="a@test.com", password="pass"
        )
        self.author = Author.objects.create(user=self.author_user, author_name="Auth")
        self.reader_user = User.objects.create_user(
            username="reader", email="r@test.com", password="pass"
        )
        Reader.objects.create(user=self.reader_user, reader_name="Reader")

        # create posts
        for i in range(8):
            Post.objects.create(
                author=self.author, title=f"T{i}", url_slug=f"slug-{i}", text="txt"
            )

    def test_home_pagination_first_page(self):
        url = reverse("home")
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        # context posts should be paginated (6 per page)
        posts = r.context["posts"]
        self.assertEqual(len(posts.object_list), 6)

    def test_login_view_get_and_post_invalid(self):
        url = reverse("login")
        # GET should return 200
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        # POST with invalid data should not redirect
        r2 = self.client.post(url, data={"email": "nope", "password": ""})
        self.assertEqual(r2.status_code, 200)

    def test_create_post_requires_author_profile(self):
        # login as reader (not an author), try to create
        self.client.force_login(self.reader_user)
        url = reverse("create_post")
        r = self.client.get(url)
        # should redirect to home because reader has no author
        self.assertEqual(r.status_code, 302)
