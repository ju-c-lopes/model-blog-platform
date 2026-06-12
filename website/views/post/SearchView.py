from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

from website.forms.post.SearchForm import SearchForm
from website.services.post.post_search import search_posts_queryset

POSTS_PER_PAGE = 6


def search_posts(request):
    form = SearchForm(request.GET)
    query = request.GET.get("query", "").strip()
    results = search_posts_queryset(query)

    paginator = Paginator(results, POSTS_PER_PAGE)
    page = request.GET.get("page")

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        "form": form,
        "query": query,
        "posts": posts,
        "results_count": results.count(),
        "is_explore": not query,
    }

    return render(request, "blog/pages/search/search_results.html", context)
