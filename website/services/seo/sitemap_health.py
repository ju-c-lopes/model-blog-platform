from django.conf import settings
from django.test import Client

from website.models.seo.SitemapEntryModel import SitemapHealthCheck
from website.services.seo.sitemap_builder import (
    SitemapUrl,
    collect_sitemap_urls,
    normalize_path,
)


def _resolve_http_host(http_host: str | None) -> str:
    if http_host:
        return http_host
    if settings.ALLOWED_HOSTS:
        return settings.ALLOWED_HOSTS[0]
    return "testserver"


def check_sitemap_urls(
    urls: list[SitemapUrl] | None = None,
    *,
    http_host: str | None = None,
) -> dict[str, int]:
    client = Client(HTTP_HOST=_resolve_http_host(http_host))
    targets = urls if urls is not None else collect_sitemap_urls()
    results: dict[str, int] = {}

    for entry in targets:
        response = client.get(entry.path)
        results[entry.path] = response.status_code
        SitemapHealthCheck.objects.update_or_create(
            path=entry.path,
            defaults={"status_code": response.status_code},
        )

    return results


def get_health_status_map(paths: list[str] | None = None) -> dict[str, SitemapHealthCheck]:
    queryset = SitemapHealthCheck.objects.all()
    if paths is not None:
        normalized = [normalize_path(path) for path in paths]
        queryset = queryset.filter(path__in=normalized)
    return {item.path: item for item in queryset}
