from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase

from website.models.author.AuthorModel import Author
from website.services.author.author_profile_editor import (
    AuthorEditBundle,
    build_bundle,
    bundle_is_valid,
    can_edit,
    get_author_for_edit,
)

User = get_user_model()


class AuthorProfileEditorTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email="editor@example.com", password="pw", username="editor"
        )
        self.other = User.objects.create_user(
            email="other@example.com", password="pw", username="other"
        )
        self.author = Author.objects.create(
            user=self.user, author_name="Editor", author_url_slug="editor"
        )

    def test_get_author_for_edit(self):
        author = get_author_for_edit("editor")
        self.assertEqual(author.pk, self.author.pk)

    def test_can_edit_owner_only(self):
        self.assertTrue(can_edit(self.user, self.author))
        self.assertFalse(can_edit(self.other, self.author))

    def test_build_bundle_get(self):
        req = self.factory.get("/nossa-equipe/editor/edit")
        req.user = self.user
        bundle = build_bundle(req, self.author)
        self.assertIsInstance(bundle, AuthorEditBundle)
        self.assertFalse(bundle.user_form.is_bound)
        self.assertEqual(bundle.social_formset.prefix, "social")

    def test_bundle_is_valid_empty_post_invalid(self):
        req = self.factory.post("/nossa-equipe/editor/edit", {})
        req.user = self.user
        bundle = build_bundle(req, self.author)
        self.assertFalse(bundle_is_valid(bundle))
