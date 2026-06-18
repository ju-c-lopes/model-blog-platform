from django.urls import path

from website.views.pages.InstitutionalViews import (
    about_page,
    contact_page,
    cookies_page,
    html_sitemap_page,
    privacy_page,
)

urlpatterns = [
    path("sobre/", about_page, name="about"),
    path("contato/", contact_page, name="contact"),
    path("privacidade/", privacy_page, name="privacy"),
    path("cookies/", cookies_page, name="cookies"),
    path("mapa-do-site/", html_sitemap_page, name="html_sitemap"),
]
