from website.models.AuthorModel import Author
from website.models.__init__ import ACADEMIC_LEVEL, SOCIAL_MEDIA
from django.shortcuts import render, redirect, get_object_or_404


def view_team(request):
    team = Author.objects.all()
    context = {
        'authors': team,
        'social_media_index': SOCIAL_MEDIA,
        'graduations_level': ACADEMIC_LEVEL,
    }
    return render(request, template_name="our-team/our-team.html", context=context)