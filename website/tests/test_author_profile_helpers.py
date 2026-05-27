from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from website.models.user.ReaderModel import Reader

User = get_user_model()


class ReaderEditHelpersTest(TestCase):
    def test_reader_edit_page_requires_login(self):
        response = self.client.get(reverse("reader-edit"))
        self.assertEqual(response.status_code, 302)

    def test_reader_edit_page_loads_for_reader(self):
        user = User.objects.create_user(
            username="r1", email="r1@test.com", password="p"
        )
        Reader.objects.create(user=user)
        self.client.force_login(user)
        response = self.client.get(reverse("reader-edit"))
        self.assertEqual(response.status_code, 200)
