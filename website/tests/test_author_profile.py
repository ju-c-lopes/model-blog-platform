from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class ProfileUpdateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="u", email="u@test.com", password="p"
        )

    def test_create_author_profile_via_view(self):
        self.client.force_login(self.user)
        url = reverse("update-profile")
        response = self.client.post(
            url, data={"profile_type": "author", "name": "New Author"}
        )
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(hasattr(self.user, "author"))
