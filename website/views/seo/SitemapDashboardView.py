from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from website.forms.seo.SitemapEntryForm import SitemapExcludeForm, SitemapIncludeForm
from website.models.seo.SitemapEntryModel import SitemapEntry
from website.services.seo.robots_txt import build_robots_txt_body
from website.services.seo.sitemap_builder import (
    collect_sitemap_urls,
    get_content_updated_at,
    lastmod_is_synced,
)
from website.services.seo.sitemap_health import (
    check_sitemap_urls,
    get_health_status_map,
)


def _require_superuser(request):
    return request.user.is_authenticated and request.user.is_superuser


def _build_dashboard_rows(urls, health_map):
    rows = []
    for url in urls:
        health = health_map.get(url.path)
        rows.append(
            {
                "url": url,
                "content_updated_at": get_content_updated_at(url),
                "lastmod_synced": lastmod_is_synced(url),
                "status_code": health.status_code if health else None,
                "checked_at": health.checked_at if health else None,
            }
        )
    return rows


@require_http_methods(["GET", "POST"])
@login_required
def sitemap_dashboard(request):
    if not _require_superuser(request):
        return HttpResponseForbidden("Acesso restrito a superusuários.")

    include_form = SitemapIncludeForm()
    exclude_form = SitemapExcludeForm()

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "verify":
            check_sitemap_urls(http_host=request.get_host())
            return redirect("seo_sitemap_dashboard")

        if action == "deactivate":
            entry_id = request.POST.get("entry_id")
            if entry_id:
                SitemapEntry.objects.filter(pk=entry_id).update(is_active=False)
            return redirect("seo_sitemap_dashboard")

        if action == "include":
            include_form = SitemapIncludeForm(request.POST)
            if include_form.is_valid():
                include_form.save()
                return redirect("seo_sitemap_dashboard")

        if action == "exclude":
            exclude_form = SitemapExcludeForm(request.POST)
            if exclude_form.is_valid():
                exclude_form.save()
                return redirect("seo_sitemap_dashboard")

    urls = collect_sitemap_urls()
    health_map = get_health_status_map([entry.path for entry in urls])
    manual_entries = SitemapEntry.objects.filter(is_active=True).order_by("path")

    context = {
        "rows": _build_dashboard_rows(urls, health_map),
        "include_form": include_form,
        "exclude_form": exclude_form,
        "manual_entries": manual_entries,
        "total_urls": len(urls),
    }
    return render(request, "blog/pages/seo/sitemap_dashboard.html", context)


def robots_txt(request):
    scheme = "https" if request.is_secure() else "http"
    sitemap_url = f"{scheme}://{request.get_host()}/sitemap.xml"
    body = build_robots_txt_body(sitemap_url)
    return HttpResponse(body, content_type="text/plain")
