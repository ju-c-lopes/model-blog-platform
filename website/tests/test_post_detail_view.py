from datetime import datetime, timedelta
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from PIL import Image

from website.models.author.AuthorModel import Author
from website.models.post.PostModel import Post
from website.models.post.TagModel import Tag

User = get_user_model()


class PostDetailViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email="author@example.com", password="pw", username="author")
        self.author = Author.objects.create(
            user=self.user,
            author_name="Author Name",
            author_url_slug="author-name",
        )
        self.docker_tag = Tag.objects.get(slug="docker")
        self.python_tag = Tag.objects.get(slug="python")

    def _make_cover(self, name="cover.png"):
        buffer = BytesIO()
        Image.new("RGB", (120, 80), color="green").save(buffer, format="PNG")
        buffer.seek(0)
        return SimpleUploadedFile(name, buffer.read(), content_type="image/png")

    def _create_post(self, **kwargs):
        defaults = {
            "author": self.author,
            "title": "Post de teste",
            "url_slug": "post-de-teste",
            "text": "<p>Conteúdo do post com texto suficiente para leitura.</p>",
            "published_date": timezone.now().date(),
        }
        defaults.update(kwargs)
        post = Post.objects.create(**defaults)
        return post

    def test_post_detail_renders_meta_dates_and_author_section(self):
        post = self._create_post()
        post.tags.add(self.docker_tag)

        response = self.client.get(reverse("post_detail", kwargs={"url_slug": post.url_slug}))

        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn("post-info-meta", content)
        self.assertIn("post-author-section", content)
        self.assertIn('class="post-detail"', content)
        self.assertIn("post-main", content)
        self.assertIn("Publicado em", content)
        self.assertIn(post.published_date.strftime("%d/%m/%Y"), content)
        self.assertIn("Author Name", content)
        self.assertNotIn("Published on", content)

    def test_post_detail_shows_cover_and_tags(self):
        post = self._create_post(cover_image=self._make_cover())
        post.tags.add(self.docker_tag, self.python_tag)

        response = self.client.get(reverse("post_detail", kwargs={"url_slug": post.url_slug}))
        content = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn("post-cover-image", content)
        self.assertIn(post.cover_image.url, content)
        self.assertIn("post-tag-list", content)
        self.assertIn("Docker", content)
        self.assertIn("Python", content)

    def test_post_detail_shows_updated_date_when_different(self):
        published = timezone.now().date() - timedelta(days=5)
        post = self._create_post(published_date=published)
        updated = timezone.make_aware(datetime.combine(published + timedelta(days=2), datetime.min.time()))
        Post.objects.filter(pk=post.pk).update(updated_date=updated)
        post.refresh_from_db()
        self.assertNotEqual(post.updated_date.date(), post.published_date)

        response = self.client.get(reverse("post_detail", kwargs={"url_slug": post.url_slug}))
        content = response.content.decode()

        self.assertIn("Atualizado em", content)
        self.assertIn(post.updated_date.strftime("%d/%m/%Y"), content)

    def test_post_detail_edit_link_for_author_only(self):
        post = self._create_post()
        url = reverse("post_detail", kwargs={"url_slug": post.url_slug})

        response = self.client.get(url)
        self.assertNotIn("Editar post", response.content.decode())

        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertIn("Editar post", response.content.decode())

    def test_posts_back_url_preserves_search_query(self):
        post = self._create_post()
        url = reverse("post_detail", kwargs={"url_slug": post.url_slug})
        search_back = reverse("search_posts") + "?query=docker"

        response = self.client.get(url, {"from_query": "docker"})
        content = response.content.decode()

        self.assertIn(f'href="{search_back}"', content)

    def test_posts_back_url_default_without_return_params(self):
        post = self._create_post()
        url = reverse("post_detail", kwargs={"url_slug": post.url_slug})
        search_url = reverse("search_posts")

        response = self.client.get(url)
        content = response.content.decode()

        self.assertIn(f'href="{search_url}"', content)
        self.assertNotIn("from_query=", content)
