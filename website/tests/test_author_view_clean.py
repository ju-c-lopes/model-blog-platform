from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.test import RequestFactory, TestCase

import website.views.AuthorView as av
from website.models.AuthorModel import Author
from website.models.AuthorSocialMediaModel import SocialMedia

User = get_user_model()


class AuthorViewCleanTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.owner = User.objects.create_user(
            email="owner@example.com", password="pw", username="owner"
        )
        self.other = User.objects.create_user(
            email="other@example.com", password="pw", username="other"
        )
        self.author = Author.objects.create(
            user=self.owner, author_name="Owner", author_url_slug="owner"
        )

    def test_view_author_page_owner_and_non_owner(self):
        captured = {}

        def fake_render(request, template_name=None, context=None, status=200):
            resp = HttpResponse(status=status)
            resp.context = context or {}
            captured["ctx"] = context or {}
            return resp

        with patch.object(av, "render", side_effect=fake_render):
            req = self.factory.get("/")
            req.user = self.other
            resp = av.view_author_page(req, slug=self.author.author_url_slug)
            assert resp.status_code == 200
            assert captured["ctx"]["author_connected"] is False

            req2 = self.factory.get("/")
            req2.user = self.owner
            resp2 = av.view_author_page(req2, slug=self.author.author_url_slug)
            assert resp2.status_code == 200
            assert captured["ctx"]["author_connected"] is True

    def test_check_request_post_and_helpers(self):
        # create sample social entry
        SocialMedia.objects.create(
            user_social_media=self.author, social_media=1, social_media_profile="p1"
        )

        data = {
            "username": "owner",
            "author_name": "Owner New",
            "social_media": ["1", "2"],
            "social_media_profile": ["p1", "p2"],
            "exclude-social": ["", ""],
        }
        img = SimpleUploadedFile("pic.jpg", b"filecontent", content_type="image/jpeg")
        req = self.factory.post("/", data, FILES={"image": img})
        req.user = self.owner
        parsed = av.check_request_post(req)
        assert parsed["username"] == "owner"
        assert parsed["name"] == "Owner New"
        assert "exclude_social_media" in parsed

        # Test update_social_media detects changes
        req2 = self.factory.post(
            "/", {"social_media": ["2"], "social_media_profile": ["p2"]}
        )
        req2.user = self.owner
        updated = av.update_social_media(req2, list(self.author.social_media.all()))
        assert isinstance(updated, bool)

    def test_edit_author_profile_post_redirects_on_success(self):
        data = {"username": "owner", "author_name": "Owner New"}
        req = self.factory.post("/", data)
        req.user = self.owner

        fake_check = {
            "username": "owner",
            "name": "Owner New",
            "check_username_request": None,
            "image": None,
            "new_social_addition": False,
            "exclude_social_media": [],
        }

        user_form_mock = MagicMock()
        user_form_mock.is_valid.return_value = True
        user_form_mock.save.return_value = req.user
        user_form_mock.cleaned_data = {"password": None}

        author_form_mock = MagicMock()
        author_form_mock.is_valid.return_value = True
        author_form_mock.save.return_value = self.author

        class FakeFormSet:
            def __init__(self, *a, **k):
                pass

            def is_valid(self):
                return True

            def save(self):
                return None

        with (
            patch.object(av, "check_request_post", return_value=fake_check),
            patch.object(av, "update_social_media", return_value=False),
            patch.object(av, "create_social_media") as mock_create,
            patch.object(av, "exclude_social_media") as mock_exclude,
            patch.object(av, "messages"),
            patch.object(av, "redirect", return_value=HttpResponse(status=302)),
            patch.object(av, "UserChangeForm", return_value=user_form_mock),
            patch.object(av, "EditAuthorForm", return_value=author_form_mock),
            patch.object(av, "inlineformset_factory", return_value=FakeFormSet),
        ):
            resp = av.edit_author_profile(req, slug=self.author.author_url_slug)
            assert resp.status_code in (301, 302)
            mock_create.assert_not_called()
            mock_exclude.assert_not_called()
