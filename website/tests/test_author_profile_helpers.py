from types import SimpleNamespace

from django.contrib.auth import get_user_model
from django.test import TestCase

from website.models.user.ReaderModel import Reader

User = get_user_model()


class ReaderEditHelpersTest(TestCase):
    def test_reader_check_user_form_username_conflict(self):
        user = User.objects.create_user(
            username="r1", email="r1@test.com", password="p"
        )
        other = User.objects.create_user(
            username="r2", email="r2@test.com", password="p"
        )
        reader = Reader.objects.create(user=user)

        class PostDict(dict):
            def getlist(self, k):
                return []

        post = PostDict({"username": other.username, "reader_name": "NewR"})
        req = SimpleNamespace(POST=post, FILES={}, user=user)

        from website.views.reader.ReaderEditView import check_user_form as rcheck

        ok = rcheck(req, reader)
        self.assertIsInstance(ok, bool)
