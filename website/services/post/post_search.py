from urllib.parse import urlencode

from django.db.models import Q, QuerySet
from django.urls import reverse

from website.services.post.post_visibility import published_posts

FROM_QUERY_PARAM = "from_query"
FROM_PAGE_PARAM = "from_page"
FROM_SEARCH_PARAM = "from_search"
MAX_QUERY_LENGTH = 100


def _tokenize_query(query: str) -> list[str]:
    return [part for part in query.split() if part.strip()]


def _term_q(term: str) -> Q:
    return (
        Q(title__icontains=term)
        | Q(text__icontains=term)
        | Q(meta_description__icontains=term)
        | Q(author__author_name__icontains=term)
        | Q(tags__name__icontains=term)
        | Q(tags__slug__icontains=term)
    )


def search_posts_queryset(query: str) -> QuerySet:
    """Return posts matching query, or all posts when query is empty (explore mode)."""
    normalized = " ".join(query.split()).strip()
    base = published_posts().select_related("author").prefetch_related("tags")

    if not normalized:
        return base.order_by("-published_date")

    q = Q()
    for token in _tokenize_query(normalized):
        q &= _term_q(token)

    return base.filter(q).distinct().order_by("-published_date")


def build_search_url(query: str = "", page=None) -> str:
    params = {}
    normalized = " ".join(query.split()).strip()[:MAX_QUERY_LENGTH]
    if normalized:
        params["query"] = normalized
    if page is not None:
        page_str = str(page).strip()
        if page_str.isdigit() and int(page_str) > 1:
            params["page"] = page_str
    base = reverse("search_posts")
    return f"{base}?{urlencode(params)}" if params else base


def build_post_detail_return_query(*, query: str = "", page=1, from_search=False) -> str:
    params = {}
    normalized = " ".join(query.split()).strip()[:MAX_QUERY_LENGTH]
    if normalized:
        params[FROM_QUERY_PARAM] = normalized
    page_str = str(page).strip()
    if page_str.isdigit() and int(page_str) > 1:
        params[FROM_PAGE_PARAM] = page_str
    elif from_search and not normalized:
        params[FROM_SEARCH_PARAM] = "1"
    return urlencode(params)


def resolve_posts_back_url(request) -> str:
    from_query = request.GET.get(FROM_QUERY_PARAM, "").strip()[:MAX_QUERY_LENGTH]
    from_page = request.GET.get(FROM_PAGE_PARAM, "").strip()
    from_search = request.GET.get(FROM_SEARCH_PARAM) == "1"

    if from_query or (from_page.isdigit() and int(from_page) > 1):
        return build_search_url(from_query, from_page or None)
    if from_search:
        return reverse("search_posts")
    return reverse("search_posts")
