from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase

from website.models.author.AuthorModel import Author
from website.models.user.ReaderModel import Reader
from website.services.user.user_registration import create_author_profile

User = get_user_model()

MINIMAL_GIF = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00"
    b",\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
)


class SignUpPasswordValidationTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_rejects_weak_password(self):
        data = {
            "email": "weak@example.com",
            "nome": "Weak User",
            "password1": "short",
            "password2": "short",
            "phone": "+5511999999999",
        }
        self.client.post(
            "/cadastre-se/",
            data=data,
            secure=True,
        )
        self.assertFalse(User.objects.filter(email="weak@example.com").exists())

    def test_accepts_strong_password(self):
        strong = "Strong$Pass1"
        data = {
            "email": "strong@example.com",
            "nome": "Strong User",
            "password1": strong,
            "password2": strong,
            "phone": "+5511999999999",
        }
        self.client.post(
            "/cadastre-se/",
            data=data,
            secure=True,
        )
        user = User.objects.filter(email="strong@example.com").first()
        self.assertIsNotNone(user)
        if user:
            self.assertTrue(user.check_password(strong))
            self.assertTrue(Reader.objects.filter(user=user).exists())

    def test_reader_signup_without_phone_succeeds(self):
        strong = "Strong$Pass1"
        data = {
            "email": "nophone@example.com",
            "nome": "No Phone User",
            "password1": strong,
            "password2": strong,
            "phone": "",
        }
        response = self.client.post(
            "/cadastre-se/",
            data=data,
            secure=True,
        )
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(email="nophone@example.com")
        self.assertIsNone(user.phone_number)
        self.assertTrue(Reader.objects.filter(user=user).exists())


class SignUpAuthorApprovalTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            email="admin@example.com",
            username="admin",
            password="Admin$Pass1",
        )
        self.strong = "Strong$Pass1"

    def test_author_signup_without_approval_does_not_create_user(self):
        data = {
            "tipo-user": "author",
            "email": "author@example.com",
            "nome": "New Author",
            "password1": self.strong,
            "password2": self.strong,
            "phone": "+5511999999999",
        }
        response = self.client.post(
            "/cadastre-se/",
            data=data,
            secure=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["aprovar"])
        self.assertFalse(User.objects.filter(email="author@example.com").exists())

    def test_author_signup_with_invalid_admin_rejected(self):
        step1 = {
            "tipo-user": "author",
            "email": "author2@example.com",
            "nome": "New Author",
            "password1": self.strong,
            "password2": self.strong,
            "phone": "+5511999999999",
        }
        self.client.post(
            "/cadastre-se/",
            data=step1,
            secure=True,
        )
        step2 = {
            **step1,
            "approval": "1",
            "super": "admin",
            "pass-super": "wrong",
        }
        self.client.post(
            "/cadastre-se/",
            data=step2,
            secure=True,
        )
        self.assertFalse(User.objects.filter(email="author2@example.com").exists())

    def test_author_signup_with_admin_approval_creates_author(self):
        step1 = {
            "tipo-user": "author",
            "email": "author3@example.com",
            "nome": "Approved Author",
            "password1": self.strong,
            "password2": self.strong,
            "phone": "+5511999999999",
        }
        self.client.post(
            "/cadastre-se/",
            data=step1,
            secure=True,
        )
        step2 = {
            **step1,
            "approval": "1",
            "super": "admin",
            "pass-super": "Admin$Pass1",
        }
        response = self.client.post(
            "/cadastre-se/",
            data=step2,
            secure=True,
        )
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(email="author3@example.com")
        self.assertTrue(user.is_staff)
        self.assertTrue(Author.objects.filter(user=user).exists())

    def test_author_signup_with_admin_email_approval_creates_author(self):
        step1 = {
            "tipo-user": "author",
            "email": "author4@example.com",
            "nome": "Email Approved Author",
            "password1": self.strong,
            "password2": self.strong,
            "phone": "+5511999999999",
        }
        self.client.post(
            "/cadastre-se/",
            data=step1,
            secure=True,
        )
        step2 = {
            **step1,
            "approval": "1",
            "super": "admin@example.com",
            "pass-super": "Admin$Pass1",
        }
        response = self.client.post(
            "/cadastre-se/",
            data=step2,
            secure=True,
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Author.objects.filter(user__email="author4@example.com").exists())


class AuthorUpgradeTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            email="admin@example.com",
            username="admin",
            password="Admin$Pass1",
        )
        self.reader_user = User.objects.create_user(
            email="reader@example.com",
            username="reader-user1",
            password="Reader$Pass1",
        )
        Reader.objects.create(
            user=self.reader_user,
            reader_name="Reader Name",
            author_upgrade_invited=True,
        )

    def test_upgrade_requires_login(self):
        response = self.client.get(
            "/solicitar-autor/",
            secure=True,
        )
        self.assertEqual(response.status_code, 302)

    def test_upgrade_with_admin_creates_author(self):
        self.client.force_login(self.reader_user)
        self.client.post(
            "/solicitar-autor/",
            {"author_name": "Blog Author"},
            secure=True,
        )
        response = self.client.post(
            "/solicitar-autor/",
            {
                "author_name": "Blog Author",
                "approval": "1",
                "super": "admin",
                "pass-super": "Admin$Pass1",
            },
            secure=True,
        )
        self.assertEqual(response.status_code, 302)
        self.reader_user.refresh_from_db()
        self.assertTrue(self.reader_user.is_staff)
        self.assertTrue(Author.objects.filter(user=self.reader_user).exists())

    def test_upgrade_with_admin_email_creates_author(self):
        self.client.force_login(self.reader_user)
        self.client.post(
            "/solicitar-autor/",
            {"author_name": "Blog Author"},
            secure=True,
        )
        response = self.client.post(
            "/solicitar-autor/",
            {
                "author_name": "Blog Author",
                "approval": "1",
                "super": "admin@example.com",
                "pass-super": "Admin$Pass1",
            },
            secure=True,
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Author.objects.filter(user=self.reader_user).exists())

    def test_upgrade_copies_reader_image_to_author(self):
        reader = self.reader_user.reader
        reader.image = SimpleUploadedFile("avatar.gif", MINIMAL_GIF, content_type="image/gif")
        reader.save()

        self.client.force_login(self.reader_user)
        self.client.post(
            "/solicitar-autor/",
            {"author_name": "Blog Author"},
            secure=True,
        )
        self.client.post(
            "/solicitar-autor/",
            {
                "author_name": "Blog Author",
                "approval": "1",
                "super": "admin",
                "pass-super": "Admin$Pass1",
            },
            secure=True,
        )

        author = Author.objects.get(user=self.reader_user)
        self.assertTrue(author.image)
        self.assertEqual(author.image.name, reader.image.name)

    def test_upgrade_uses_reader_name_when_author_name_empty_on_approval(self):
        self.client.force_login(self.reader_user)
        self.client.post(
            "/solicitar-autor/",
            {"author_name": "Reader Name"},
            secure=True,
        )
        self.client.post(
            "/solicitar-autor/",
            {
                "author_name": "",
                "approval": "1",
                "super": "admin",
                "pass-super": "Admin$Pass1",
            },
            secure=True,
        )

        author = Author.objects.get(user=self.reader_user)
        self.assertEqual(author.author_name, "Reader Name")


class CreateAuthorProfileTests(TestCase):
    def test_create_author_profile_syncs_reader_image_and_name(self):
        user = User.objects.create_user(
            email="sync@example.com",
            username="sync-user",
            password="Reader$Pass1",
        )
        reader = Reader.objects.create(user=user, reader_name="Synced Name")
        reader.image = SimpleUploadedFile("sync.gif", MINIMAL_GIF, content_type="image/gif")
        reader.save()

        author = create_author_profile(user, "")

        self.assertEqual(author.author_name, "Synced Name")
        self.assertEqual(author.image.name, reader.image.name)
