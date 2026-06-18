from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time
from decimal import Decimal
from typing import Any

from django.urls import reverse
from django.utils import timezone

from website.models.author.AuthorModel import Author
from website.models.post.PostModel import Post
from website.models.seo.SitemapEntryModel import SitemapEntry
from website.services.post.post_visibility import published_posts


@dataclass(frozen=True)
class SitemapUrl:
    path: str
    lastmod: datetime | None
    source: str
    linked_object: Any | None = None
    priority: Decimal | None = None
    changefreq: str = ""


def normalize_path(path: str) -> str:
    normalized = path.strip()
    if not normalized:
        return "/"
    if not normalized.startswith("/"):
        normalized = f"/{normalized}"
    return normalized


def _date_to_lastmod(value) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        if timezone.is_naive(value):
            return timezone.make_aware(value, timezone.get_current_timezone())
        return value
    return timezone.make_aware(datetime.combine(value, time.min), timezone.get_current_timezone())


def _collect_automatic_urls() -> list[SitemapUrl]:
    urls: list[SitemapUrl] = []

    static_routes = (
        ("home", "static"),
        ("team", "static"),
        ("search_posts", "static"),
        ("about", "static"),
        ("contact", "static"),
        ("privacy", "static"),
        ("cookies", "static"),
        ("html_sitemap", "static"),
    )
    for route_name, source in static_routes:
        urls.append(
            SitemapUrl(
                path=normalize_path(reverse(route_name)),
                lastmod=None,
                source=source,
            )
        )

    for author in Author.objects.all().only("pk", "author_url_slug", "author_name", "created_at"):
        urls.append(
            SitemapUrl(
                path=normalize_path(reverse("author", kwargs={"slug": author.author_url_slug})),
                lastmod=_date_to_lastmod(author.created_at),
                source="author",
                linked_object=author,
            )
        )

    for post in published_posts().only("pk", "url_slug", "title", "updated_date"):
        urls.append(
            SitemapUrl(
                path=normalize_path(reverse("post_detail", kwargs={"url_slug": post.url_slug})),
                lastmod=_date_to_lastmod(post.updated_date),
                source="post",
                linked_object=post,
            )
        )

    return urls


def _apply_overrides(urls: list[SitemapUrl]) -> list[SitemapUrl]:
    by_path: dict[str, SitemapUrl] = {entry.path: entry for entry in urls}

    for exclusion in SitemapEntry.objects.filter(entry_type=SitemapEntry.EXCLUDE, is_active=True):
        by_path.pop(normalize_path(exclusion.path), None)

    for inclusion in SitemapEntry.objects.filter(entry_type=SitemapEntry.INCLUDE, is_active=True):
        path = normalize_path(inclusion.path)
        by_path[path] = SitemapUrl(
            path=path,
            lastmod=_date_to_lastmod(inclusion.lastmod),
            source="manual",
            linked_object=inclusion,
            priority=inclusion.priority,
            changefreq=inclusion.changefreq,
        )

    return sorted(by_path.values(), key=lambda item: item.path)


def collect_sitemap_urls() -> list[SitemapUrl]:
    return _apply_overrides(_collect_automatic_urls())


def get_content_updated_at(url: SitemapUrl) -> datetime | None:
    if url.source == "post" and isinstance(url.linked_object, Post):
        return _date_to_lastmod(url.linked_object.updated_date)
    if url.source == "author" and isinstance(url.linked_object, Author):
        return _date_to_lastmod(url.linked_object.created_at)
    if url.source == "manual" and isinstance(url.linked_object, SitemapEntry):
        return _date_to_lastmod(url.linked_object.updated_at)
    return None


def lastmod_is_synced(url: SitemapUrl) -> bool | None:
    content_updated = get_content_updated_at(url)
    if content_updated is None or url.lastmod is None:
        return None
    return url.lastmod.date() >= content_updated.date()
