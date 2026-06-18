from django.shortcuts import render

from website.services.seo.html_sitemap import build_html_sitemap_sections


def about_page(request):
    return render(request, "blog/pages/institutional/about.html")


def contact_page(request):
    return render(request, "blog/pages/institutional/contact.html")


def privacy_page(request):
    return render(request, "blog/pages/institutional/privacy.html")


def cookies_page(request):
    return render(request, "blog/pages/institutional/cookies.html")


def html_sitemap_page(request):
    sections = build_html_sitemap_sections()
    return render(
        request,
        "blog/pages/institutional/html_sitemap.html",
        {"sections": sections},
    )
