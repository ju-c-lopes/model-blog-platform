from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from website.models.author.AuthorModel import Author
from website.models.user.ReaderModel import Reader

User = get_user_model()


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
        self.client.post("/cadastre-se/", data=data)
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
        self.client.post("/cadastre-se/", data=data)
        user = User.objects.filter(email="strong@example.com").first()
        self.assertIsNotNone(user)
        if user:
            self.assertTrue(user.check_password(strong))
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
        response = self.client.post("/cadastre-se/", data=data)
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
        self.client.post("/cadastre-se/", data=step1)
        step2 = {
            **step1,
            "approval": "1",
            "super": "admin",
            "pass-super": "wrong",
        }
        self.client.post("/cadastre-se/", data=step2)
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
        self.client.post("/cadastre-se/", data=step1)
        step2 = {
            **step1,
            "approval": "1",
            "super": "admin",
            "pass-super": "Admin$Pass1",
        }
        response = self.client.post("/cadastre-se/", data=step2)
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(email="author3@example.com")
        self.assertTrue(user.is_staff)
        self.assertTrue(Author.objects.filter(user=user).exists())


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
        Reader.objects.create(user=self.reader_user, reader_name="Reader Name")

    def test_upgrade_requires_login(self):
        response = self.client.get("/solicitar-autor/")
        self.assertEqual(response.status_code, 302)

    def test_upgrade_with_admin_creates_author(self):
        self.client.force_login(self.reader_user)
        self.client.post("/solicitar-autor/", {"author_name": "Blog Author"})
        response = self.client.post(
            "/solicitar-autor/",
            {
                "author_name": "Blog Author",
                "approval": "1",
                "super": "admin",
                "pass-super": "Admin$Pass1",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.reader_user.refresh_from_db()
        self.assertTrue(self.reader_user.is_staff)
        self.assertTrue(Author.objects.filter(user=self.reader_user).exists())
