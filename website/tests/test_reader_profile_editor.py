from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase

from website.models.user.ReaderModel import Reader
from website.services.reader.reader_profile_editor import (
    ReaderEditBundle,
    build_bundle,
    bundle_is_valid,
    can_edit,
    get_reader_for_edit,
)

User = get_user_model()


class ReaderProfileEditorTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(email="reader@example.com", password="pw", username="reader")
        self.other = User.objects.create_user(email="other@example.com", password="pw", username="other")
        self.reader = Reader.objects.create(user=self.user)

    def test_get_reader_for_edit(self):
        reader = get_reader_for_edit(self.user)
        self.assertEqual(reader.pk, self.reader.pk)

    def test_can_edit_owner_only(self):
        self.assertTrue(can_edit(self.user, self.reader))
        self.assertFalse(can_edit(self.other, self.reader))

    def test_build_bundle_get(self):
        req = self.factory.get("/editar-leitor/")
        req.user = self.user
        bundle = build_bundle(req, self.reader)
        self.assertIsInstance(bundle, ReaderEditBundle)
        self.assertFalse(bundle.user_form.is_bound)

    def test_bundle_is_valid_empty_post_invalid(self):
        req = self.factory.post("/editar-leitor/", {})
        req.user = self.user
        bundle = build_bundle(req, self.reader)
        self.assertFalse(bundle_is_valid(bundle))
