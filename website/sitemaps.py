from django.contrib.sitemaps import Sitemap

from website.services.seo.sitemap_builder import SitemapUrl, collect_sitemap_urls


class UnifiedSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self) -> list[SitemapUrl]:
        return collect_sitemap_urls()

    def location(self, obj: SitemapUrl) -> str:
        return obj.path

    def lastmod(self, obj: SitemapUrl):
        return obj.lastmod

    def priority(self, obj: SitemapUrl) -> float:
        if obj.priority is not None:
            return float(obj.priority)
        if obj.source == "post":
            return 0.8
        if obj.source == "author":
            return 0.6
        if obj.source == "manual":
            return 0.5
        return 0.5

    def changefreq(self, obj: SitemapUrl) -> str:
        return obj.changefreq or "weekly"
