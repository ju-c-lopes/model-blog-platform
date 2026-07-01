import shutil
from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from PIL import Image

from website.models.author.AuthorModel import Author
from website.models.post.PostModel import Post
from website.services.post import post_content_images as content_images

User = None


def _make_image(name="test.png"):
    buffer = BytesIO()
    Image.new("RGB", (40, 40), color="red").save(buffer, format="PNG")
    buffer.seek(0)
    return SimpleUploadedFile(name, buffer.read(), content_type="image/png")


@override_settings(MEDIA_ROOT="/tmp/test-post-content-media")
class PostContentImageServiceTests(TestCase):
    def setUp(self):
        root = Path(settings.MEDIA_ROOT)
        if root.exists():
            shutil.rmtree(root)
        root.mkdir(parents=True, exist_ok=True)

    def test_save_to_temp_and_consolidate_to_slug(self):
        session_id = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        uploaded = _make_image("diagrama-docker.png")
        image_url = content_images.save_content_image(uploaded, session_id=session_id)

        self.assertIn("/media/post_content/_tmp/", image_url)
        self.assertIn(session_id, image_url)
        self.assertIn("diagrama-docker.png", image_url)

        html = f'<p>Olá</p><img src="{image_url}" alt="diagrama" />'
        consolidated = content_images.consolidate_temp_images(
            html,
            session_id,
            "meu-post-docker",
        )

        self.assertIn("/media/post_content/meu-post-docker/diagrama-docker.png", consolidated)
        self.assertNotIn("/media/post_content/_tmp/", consolidated)
        self.assertTrue(
            (Path(settings.MEDIA_ROOT) / "post_content" / "meu-post-docker" / "diagrama-docker.png").exists()
        )

    def test_duplicate_filename_gets_numeric_suffix(self):
        session_id = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        slug = "meu-post-docker"

        first_url = content_images.save_content_image(_make_image("foto.png"), session_id=session_id)
        second_url = content_images.save_content_image(_make_image("foto.png"), session_id=session_id)

        self.assertIn("foto.png", first_url)
        self.assertIn("foto-2.png", second_url)

        html = f'<img src="{first_url}" /><img src="{second_url}" />'
        consolidated = content_images.consolidate_temp_images(html, session_id, slug)

        self.assertIn("/media/post_content/meu-post-docker/foto.png", consolidated)
        self.assertIn("/media/post_content/meu-post-docker/foto-2.png", consolidated)


class PostContentImageUploadViewTests(TestCase):
    def setUp(self):
        global User
        from django.contrib.auth import get_user_model

        User = get_user_model()
        self.client = Client()
        self.user = User.objects.create_user(email="author@example.com", password="pw", username="author")
        self.author = Author.objects.create(
            user=self.user,
            author_name="Author",
            author_url_slug="author",
        )

    @override_settings(MEDIA_ROOT="/tmp/test-post-content-upload-media")
    def test_upload_to_temp_on_create_session(self):
        Path(settings.MEDIA_ROOT).mkdir(parents=True, exist_ok=True)
        self.client.force_login(self.user)
        session = self.client.session
        session["post_content_upload_session"] = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        session.save()

        response = self.client.post(
            reverse("post_upload_content_image"),
            {
                "upload_session_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
                "image": _make_image(),
            },
            secure=True,
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload["success"])
        self.assertIn("/media/post_content/_tmp/", payload["url"])

    @override_settings(MEDIA_ROOT="/tmp/test-post-content-upload-media")
    def test_upload_restores_session_from_post_body(self):
        Path(settings.MEDIA_ROOT).mkdir(parents=True, exist_ok=True)
        self.client.force_login(self.user)

        create_page = self.client.get(
            reverse("create_post"),
            secure=True,
        )
        session_id = create_page.context["upload_session_id"]

        upload_client = Client()
        upload_client.force_login(self.user)

        response = upload_client.post(
            reverse("post_upload_content_image"),
            {
                "upload_session_id": session_id,
                "image": _make_image(),
            },
            secure=True,
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload["success"])
        self.assertIn("/media/post_content/_tmp/", payload["url"])

    @override_settings(MEDIA_ROOT="/tmp/test-post-content-upload-media")
    def test_upload_directly_to_slug_on_edit(self):
        Path(settings.MEDIA_ROOT).mkdir(parents=True, exist_ok=True)
        post = Post.objects.create(
            author=self.author,
            title="Post",
            url_slug="post-slug",
            text="<p>conteúdo</p>",
            status=Post.PUBLISHED,
        )
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("post_upload_content_image"),
            {
                "url_slug": post.url_slug,
                "image": _make_image(),
            },
            secure=True,
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("/media/post_content/post-slug/", payload["url"])

    @override_settings(MEDIA_ROOT="/tmp/test-post-content-upload-media")
    def test_create_post_consolidates_temp_images(self):
        Path(settings.MEDIA_ROOT).mkdir(parents=True, exist_ok=True)
        self.client.force_login(self.user)

        create_page = self.client.get(
            reverse("create_post"),
            secure=True,
        )
        session_id = create_page.context["upload_session_id"]

        upload_response = self.client.post(
            reverse("post_upload_content_image"),
            {
                "upload_session_id": session_id,
                "image": _make_image(),
            },
            secure=True,
        )
        image_url = upload_response.json()["url"]

        response = self.client.post(
            reverse("create_post"),
            {
                "title": "Post Docker",
                "url_slug": "post-docker",
                "meta_description": "Relato docker",
                "text": f"<p>Texto longo do post.</p><img src='{image_url}' alt='img' />",
                "upload_session_id": session_id,
                "status": Post.PUBLISHED,
            },
            secure=True,
        )

        self.assertEqual(response.status_code, 302)
        post = Post.objects.get(url_slug="post-docker")
        self.assertIn("/media/post_content/post-docker/", post.text)
        self.assertNotIn("/media/post_content/_tmp/", post.text)
