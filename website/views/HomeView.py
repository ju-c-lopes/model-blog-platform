from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

from website.models.post.PostModel import Post

POSTS_PER_PAGE = 6


def get_home_page(request):
    post_list = Post.objects.select_related("author").prefetch_related("tags").order_by("-published_date")

    paginator = Paginator(post_list, POSTS_PER_PAGE)
    page = request.GET.get("page")

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "blog/pages/home-page/homepage.html", {"posts": posts})
