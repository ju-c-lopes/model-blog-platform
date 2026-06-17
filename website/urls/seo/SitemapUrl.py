from django.urls import path

from website.views.seo.SitemapDashboardView import sitemap_dashboard

urlpatterns = [
    path("sitemap/", sitemap_dashboard, name="seo_sitemap_dashboard"),
]
