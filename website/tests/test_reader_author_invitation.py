from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from website.models.user.ReaderModel import Reader

User = get_user_model()


class ReaderAuthorInvitationTests(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_superuser(
            email="admin@example.com",
            username="admin",
            password="Admin$Pass1",
        )
        self.reader_user = User.objects.create_user(
            email="reader@example.com",
            username="reader-user",
            password="Reader$Pass1",
        )
        self.reader = Reader.objects.create(
            user=self.reader_user,
            reader_name="Reader Name",
            author_upgrade_invited=False,
        )

    def test_reader_without_invitation_cannot_access_upgrade_page(self):
        self.client.force_login(self.reader_user)
        response = self.client.get(
            reverse("author-upgrade"),
            secure=True,
        )
        self.assertRedirects(
            response,
            reverse("reader-edit"),
            fetch_redirect_response=False,
        )

    def test_reader_without_invitation_does_not_see_upgrade_link(self):
        self.client.force_login(self.reader_user)
        response = self.client.get(
            reverse("reader-edit"),
            secure=True,
        )
        content = response.content.decode()
        self.assertNotIn("Solicitar perfil de autor", content)
        self.assertNotIn(reverse("author-upgrade"), content)

    def test_reader_with_invitation_sees_upgrade_link(self):
        self.reader.author_upgrade_invited = True
        self.reader.save(update_fields=["author_upgrade_invited"])
        self.client.force_login(self.reader_user)
        response = self.client.get(
            reverse("reader-edit"),
            secure=True,
        )
        content = response.content.decode()
        self.assertIn("Solicitar perfil de autor", content)
        self.assertIn(reverse("author-upgrade"), content)

    def test_reader_with_invitation_can_open_upgrade_page(self):
        self.reader.author_upgrade_invited = True
        self.reader.save(update_fields=["author_upgrade_invited"])
        self.client.force_login(self.reader_user)
        response = self.client.get(
            reverse("author-upgrade"),
            secure=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Solicitar perfil de autor", response.content.decode())
