from django.shortcuts import get_object_or_404, render

from website.models.author.AuthorModel import Author


def view_author_page(request, slug):
    author = get_object_or_404(
        Author.objects.prefetch_related("graduations", "jobs", "social_media"),
        author_url_slug=slug,
    )
    author_connected = request.user.is_authenticated and request.user == author.user
    context = {
        "author": author,
        "author_connected": author_connected,
    }
    return render(
        request,
        template_name="blog/pages/author/author.html",
        context=context,
        status=200,
    )
