from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

from website.models.PostModel import Post


def get_home_page(request):
    # Get all posts ordered by published date (newest first)
    post_list = Post.objects.all().order_by("-published_date")

    # Set up pagination - 6 posts per page
    paginator = Paginator(post_list, 6)
    page = request.GET.get("page")

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, "home-page/homepage.html", {"posts": posts})
