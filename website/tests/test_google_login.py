from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase

from website.adapters.social_account import CustomSocialAccountAdapter
from website.models.author.AuthorModel import Author
from website.models.user.ReaderModel import Reader

User = get_user_model()


class CustomSocialAccountAdapterTests(TestCase):
    def setUp(self):
        self.adapter = CustomSocialAccountAdapter()
        self.factory = RequestFactory()

    def test_save_user_creates_reader_not_author(self):
        user = User.objects.create_user(
            email="new@example.com",
            username="new-user99",
            password="Temp$Pass123",
        )
        user.set_unusable_password()
        user.save(update_fields=["password"])

        sociallogin = MagicMock()
        sociallogin.user = user
        sociallogin.account.extra_data = {"name": "New Google User"}

        request = self.factory.get("/")
        with patch(
            "website.adapters.social_account.DefaultSocialAccountAdapter.save_user",
            return_value=user,
        ):
            self.adapter.save_user(request, sociallogin)

        self.assertTrue(Reader.objects.filter(user=user).exists())
        self.assertFalse(Author.objects.filter(user=user).exists())

    def test_pre_social_login_connects_existing_email(self):
        existing = User.objects.create_user(
            email="exists@example.com",
            username="exists-user1",
            password="Exists$Pass1",
        )
        sociallogin = MagicMock()
        sociallogin.is_existing = False
        sociallogin.user.email = "exists@example.com"
        sociallogin.account.extra_data = {"email": "exists@example.com"}
        sociallogin.connect = MagicMock()

        request = self.factory.get("/")
        self.adapter.pre_social_login(request, sociallogin)

        sociallogin.connect.assert_called_once_with(request, existing)


class GoogleOAuthTemplateTests(TestCase):
    def test_login_hides_google_button_without_client_id(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "g_id_signin")

    def test_login_shows_google_button_with_client_id(self):
        with self.settings(GOOGLE_OAUTH_CLIENT_ID="test-id.apps.googleusercontent.com"):
            response = self.client.get("/login/")
            self.assertContains(response, "g_id_signin")
            self.assertContains(response, "test-id.apps.googleusercontent.com")
            self.assertContains(response, 'data-ux_mode="redirect"')
            self.assertContains(response, "/accounts/google/login/token/")
