from django import template
from django.urls import reverse

from website.services.post.post_search import build_post_detail_return_query

register = template.Library()


@register.simple_tag
def post_detail_url(slug, search_query="", search_page=1, from_search=False):
    base = reverse("post_detail", kwargs={"url_slug": slug})
    return_qs = build_post_detail_return_query(
        query=search_query or "",
        page=search_page,
        from_search=bool(from_search),
    )
    if return_qs:
        return f"{base}?{return_qs}"
    return base
