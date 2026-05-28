from django.shortcuts import render

from website.models import ACADEMIC_LEVEL, SOCIAL_MEDIA
from website.models.author.AuthorModel import Author


def view_team(request):
    team = Author.objects.all()
    context = {
        "authors": team,
        "social_media_index": SOCIAL_MEDIA,
        "graduations_level": ACADEMIC_LEVEL,
    }
    return render(request, template_name="blog/pages/our-team/our-team.html", context=context)
