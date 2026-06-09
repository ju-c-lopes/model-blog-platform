from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from PIL import Image

from website.models.author.AuthorModel import Author
from website.models.post.PostModel import Post
from website.models.post.TagModel import Tag

User = get_user_model()


class PostEditFormTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email="author@example.com", password="pw", username="author")
        self.author = Author.objects.create(
            user=self.user,
            author_name="Author",
            author_url_slug="author",
        )
        self.docker_tag = Tag.objects.get(slug="docker")
        self.python_tag = Tag.objects.get(slug="python")

    def _make_image(self, name="cover.png"):
        buffer = BytesIO()
        Image.new("RGB", (100, 100), color="blue").save(buffer, format="PNG")
        buffer.seek(0)
        return SimpleUploadedFile(name, buffer.read(), content_type="image/png")

    def test_create_post_with_cover_and_tags(self):
        self.client.force_login(self.user)
        url = reverse("create_post")
        response = self.client.post(
            url,
            {
                "title": "Experiência com Docker",
                "url_slug": "experiencia-docker",
                "meta_description": "Relato sobre Docker no dia a dia.",
                "text": "<p>Conteúdo do post com mais de dez caracteres.</p>",
                "tags": [str(self.docker_tag.pk), str(self.python_tag.pk)],
                "cover_image": self._make_image(),
            },
        )

        self.assertEqual(response.status_code, 302)
        post = Post.objects.get(url_slug="experiencia-docker")
        self.assertTrue(post.cover_image)
        self.assertEqual(post.tags.count(), 2)
        self.assertIn(self.docker_tag, post.tags.all())

    def test_edit_post_page_shows_tags_and_preview_controls(self):
        post = Post.objects.create(
            author=self.author,
            title="Post teste",
            url_slug="post-teste",
            text="<p>Conteúdo inicial do post.</p>",
        )
        post.tags.add(self.docker_tag)

        self.client.force_login(self.user)
        response = self.client.get(reverse("edit_post", kwargs={"url_slug": post.url_slug}))

        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn("Editar HTML", content)
        self.assertIn("Imagem de capa", content)
        self.assertIn("Docker", content)
        self.assertIn('value="{}"'.format(self.docker_tag.pk), content)
