from django.shortcuts import render

from website.models.author.AuthorModel import Author


def view_team(request):
    authors = Author.objects.prefetch_related("graduations", "jobs", "social_media").all()
    context = {
        "authors": authors,
    }
    return render(request, template_name="blog/pages/our-team/our-team.html", context=context)
