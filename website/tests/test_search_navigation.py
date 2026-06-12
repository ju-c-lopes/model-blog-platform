from types import SimpleNamespace

from django.test import SimpleTestCase
from django.urls import reverse

from website.services.post.post_search import (
    build_post_detail_return_query,
    build_search_url,
    resolve_posts_back_url,
)


class SearchNavigationTests(SimpleTestCase):
    def test_build_search_url_with_query(self):
        url = build_search_url("docker compose")
        self.assertEqual(url, f"{reverse('search_posts')}?query=docker+compose")

    def test_build_search_url_with_query_and_page(self):
        url = build_search_url("docker", page=2)
        self.assertEqual(url, f"{reverse('search_posts')}?query=docker&page=2")

    def test_build_post_detail_return_query_from_search_explore(self):
        qs = build_post_detail_return_query(from_search=True)
        self.assertEqual(qs, "from_search=1")

    def test_build_post_detail_return_query_with_search_term(self):
        qs = build_post_detail_return_query(query="SEO", page=1, from_search=True)
        self.assertEqual(qs, "from_query=SEO")

    def test_build_post_detail_return_query_with_page(self):
        qs = build_post_detail_return_query(query="SEO", page=3)
        self.assertEqual(qs, "from_query=SEO&from_page=3")

    def test_resolve_posts_back_url_from_query(self):
        request = SimpleNamespace(GET={"from_query": "docker"})
        self.assertEqual(resolve_posts_back_url(request), build_search_url("docker"))

    def test_resolve_posts_back_url_from_explore(self):
        request = SimpleNamespace(GET={"from_search": "1"})
        self.assertEqual(resolve_posts_back_url(request), reverse("search_posts"))

    def test_resolve_posts_back_url_default(self):
        request = SimpleNamespace(GET={})
        self.assertEqual(resolve_posts_back_url(request), reverse("search_posts"))
