from datetime import date
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

import website.views.author.AuthorView as av
from website.models.author.AuthorModel import Author
from website.models.author.GraduationsModel import Graduation
from website.models.author.JobsModel import Job

User = get_user_model()


class AuthorViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.owner = User.objects.create_user(email="owner@example.com", password="pw", username="owner")
        self.other = User.objects.create_user(email="other@example.com", password="pw", username="other")
        self.author = Author.objects.create(
            user=self.owner,
            author_name="Owner Author",
            author_url_slug="owner",
            history="História de teste do autor.",
        )
        Graduation.objects.create(
            author=self.author,
            graduation_level=1,
            school="Universidade Teste",
            course="Ciência da Computação",
            year_graduation=2020,
            concluded=True,
        )
        Job.objects.create(
            employee=self.author,
            occupation="Desenvolvedor",
            company="Empresa Teste",
            location="São Paulo",
            start_date=date(2021, 1, 15),
            current_job=True,
            roles_description="Desenvolvimento de features web.",
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
            self.assertEqual(resp.status_code, 200)
            self.assertFalse(captured["ctx"]["author_connected"])

            req2 = self.factory.get("/")
            req2.user = self.owner
            resp2 = av.view_author_page(req2, slug=self.author.author_url_slug)
            self.assertEqual(resp2.status_code, 200)
            self.assertTrue(captured["ctx"]["author_connected"])

    def test_author_page_renders_profile_content(self):
        url = reverse("author", kwargs={"slug": self.author.author_url_slug})
        response = self.client.get(url, secure=True)

        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn("Owner Author", content)
        self.assertIn("História de teste do autor.", content)
        self.assertIn("Ciência da Computação", content)
        self.assertIn("Desenvolvedor", content)
        self.assertIn("Empresa Teste", content)
        self.assertIn("Desenvolvimento de features web.", content)

    def test_author_page_edit_link_for_owner_only(self):
        url = reverse("author", kwargs={"slug": self.author.author_url_slug})

        response_visitor = self.client.get(url, secure=True)
        self.assertNotContains(response_visitor, "Editar perfil")

        self.client.force_login(self.owner)
        response_owner = self.client.get(url, secure=True)
        self.assertContains(response_owner, "Editar perfil")
        self.assertContains(
            response_owner,
            reverse("edit_author", kwargs={"slug": self.author.author_url_slug}),
        )

    def test_team_page_lists_authors(self):
        response = self.client.get(reverse("team"), secure=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nossa equipe")
        self.assertContains(response, "Owner Author")
