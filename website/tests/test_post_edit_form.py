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
                "status": Post.PUBLISHED,
                "cover_image": self._make_image(),
            },
            secure=True,
        )

        self.assertEqual(response.status_code, 302)
        post = Post.objects.get(url_slug="experiencia-docker")
        self.assertTrue(post.cover_image)
        self.assertEqual(post.tags.count(), 2)
        self.assertIn(self.docker_tag, post.tags.all())

    def test_update_post_shows_flash_message_on_detail(self):
        post = Post.objects.create(
            author=self.author,
            title="Post original",
            url_slug="post-original",
            text="<p>Conteúdo do post com mais de dez caracteres.</p>",
            status=Post.DRAFT,
        )
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("edit_post", kwargs={"url_slug": post.url_slug}),
            {
                "title": "Post atualizado",
                "url_slug": post.url_slug,
                "meta_description": "Descrição válida.",
                "text": "<p>Conteúdo atualizado com mais de dez caracteres.</p>",
                "status": Post.DRAFT,
            },
            secure=True,
        )
        self.assertEqual(response.status_code, 302)
        detail = self.client.get(
            reverse("post_detail", kwargs={"url_slug": post.url_slug}),
            secure=True,
        )
        self.assertContains(detail, "Post atualizado com sucesso!")
        home = self.client.get(
            reverse("home"),
            secure=True,
        )
        self.assertNotContains(home, "Post atualizado com sucesso!")

    def test_invalid_create_post_preserves_selected_tags(self):
        Post.objects.create(
            author=self.author,
            title="Outro post",
            url_slug="slug-ocupado",
            text="<p>Conteúdo de outro post.</p>",
        )
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("create_post"),
            {
                "title": "Novo post",
                "url_slug": "slug-ocupado",
                "meta_description": "Descrição válida.",
                "text": "<p>Conteúdo do post com mais de dez caracteres.</p>",
                "tags": [str(self.python_tag.pk)],
                "status": Post.DRAFT,
            },
            secure=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.python_tag.pk, response.context["selected_tag_ids"])

    def test_create_post_with_new_tag_name(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("create_post"),
            {
                "title": "Post com tag nova",
                "url_slug": "post-tag-nova",
                "meta_description": "Descrição válida.",
                "text": "<p>Conteúdo do post com mais de dez caracteres.</p>",
                "new_tag_names": ["Rust"],
                "status": Post.PUBLISHED,
            },
            secure=True,
        )

        self.assertEqual(response.status_code, 302)
        post = Post.objects.get(url_slug="post-tag-nova")
        self.assertEqual(post.tags.count(), 1)
        self.assertTrue(Tag.objects.filter(slug="rust", name="Rust").exists())

    def test_invalid_create_post_preserves_pending_new_tag_names(self):
        Post.objects.create(
            author=self.author,
            title="Outro post",
            url_slug="slug-ocupado",
            text="<p>Conteúdo de outro post.</p>",
        )
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("create_post"),
            {
                "title": "Novo post",
                "url_slug": "slug-ocupado",
                "meta_description": "Descrição válida.",
                "text": "<p>Conteúdo do post com mais de dez caracteres.</p>",
                "new_tag_names": ["Rust"],
                "status": Post.DRAFT,
            },
            secure=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Rust", response.context["pending_new_tag_names"])

    def test_invalid_edit_post_preserves_selected_tags(self):
        Post.objects.create(
            author=self.author,
            title="Outro post",
            url_slug="slug-ocupado",
            text="<p>Conteúdo de outro post.</p>",
        )
        post = Post.objects.create(
            author=self.author,
            title="Post teste",
            url_slug="post-teste",
            text="<p>Conteúdo inicial do post.</p>",
            status=Post.PUBLISHED,
        )
        post.tags.add(self.docker_tag)

        self.client.force_login(self.user)
        response = self.client.post(
            reverse("edit_post", kwargs={"url_slug": post.url_slug}),
            {
                "title": "Post teste",
                "url_slug": "slug-ocupado",
                "meta_description": "Descrição válida.",
                "text": "<p>Conteúdo atualizado com mais de dez caracteres.</p>",
                "tags": [str(self.python_tag.pk)],
                "status": Post.PUBLISHED,
            },
            secure=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.python_tag.pk, response.context["selected_tag_ids"])
        self.assertNotIn(self.docker_tag.pk, response.context["selected_tag_ids"])

    def test_edit_post_page_shows_tags_and_preview_controls(self):
        post = Post.objects.create(
            author=self.author,
            title="Post teste",
            url_slug="post-teste",
            text="<p>Conteúdo inicial do post.</p>",
            status=Post.PUBLISHED,
        )
        post.tags.add(self.docker_tag)

        self.client.force_login(self.user)
        response = self.client.get(reverse("edit_post", kwargs={"url_slug": post.url_slug}), secure=True)

        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn("Editar HTML", content)
        self.assertIn("Imagem de capa", content)
        self.assertIn("tag-picker", content)
        self.assertIn("Docker", content)
        self.assertIn('data-tag-id="{}"'.format(self.docker_tag.pk), content)
