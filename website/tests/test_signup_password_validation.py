from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()


class SignUpPasswordValidationTests(TestCase):
    def setUp(self):
        # use the test client so middleware (messages, sessions) are exercised
        self.client = Client()

    def test_rejects_weak_password(self):
        data = {
            "email": "weak@example.com",
            "nome": "Weak User",
            "password1": "short",
            "password2": "short",
            "phone": "+5511999999999",
        }
        # sign-up URL is mounted at /cadastre-se/ in the project urls
        self.client.post("/cadastre-se/", data=data)
        self.assertFalse(User.objects.filter(email="weak@example.com").exists())

    def test_accepts_strong_password(self):
        # pick a strong password that fits the app's legacy max-length (<=16)
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
