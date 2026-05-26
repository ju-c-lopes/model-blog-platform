from django.shortcuts import get_object_or_404, render

from website.models import SOCIAL_MEDIA
from website.models.author.AuthorModel import Author


def view_author_page(request, slug):
    author = get_object_or_404(Author, author_url_slug=slug)
    context = {
        "author": author,
        "author_connected": False,
        "social_media_index": SOCIAL_MEDIA,
    }
    if request.user != author.user:
        return render(
            request,
            template_name="blog/pages/author/author.html",
            context=context,
            status=200,
        )
    context["author_connected"] = True
    return render(
        request,
        template_name="blog/pages/author/author.html",
        context=context,
        status=200,
    )
