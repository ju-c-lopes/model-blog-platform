from __future__ import annotations

from dataclasses import dataclass

from django.urls import reverse

from website.models.author.AuthorModel import Author
from website.models.post.PostModel import Post
from website.services.seo.sitemap_builder import (
    SitemapUrl,
    collect_sitemap_urls,
    normalize_path,
)


@dataclass(frozen=True)
class HtmlSitemapLink:
    path: str
    label: str


INSTITUTIONAL_ROUTES: tuple[tuple[str, str], ...] = (
    ("about", "Sobre"),
    ("contact", "Contato"),
    ("privacy", "Política de privacidade"),
    ("cookies", "Política de cookies"),
)


def _link_label(entry: SitemapUrl) -> str:
    if entry.source == "post" and isinstance(entry.linked_object, Post):
        return entry.linked_object.title
    if entry.source == "author" and isinstance(entry.linked_object, Author):
        return entry.linked_object.author_name
    return entry.path


def _to_link(entry: SitemapUrl) -> HtmlSitemapLink:
    return HtmlSitemapLink(path=entry.path, label=_link_label(entry))


def build_institutional_links() -> list[HtmlSitemapLink]:
    return [
        HtmlSitemapLink(path=normalize_path(reverse(route_name)), label=label)
        for route_name, label in INSTITUTIONAL_ROUTES
    ]


def build_html_sitemap_sections() -> dict[str, list[HtmlSitemapLink]]:
    urls = collect_sitemap_urls()
    return {
        "institutional": build_institutional_links(),
        "authors": [_to_link(entry) for entry in urls if entry.source == "author"],
        "series": [],
        "posts": [_to_link(entry) for entry in urls if entry.source == "post"],
    }
