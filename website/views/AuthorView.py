from website.models.AuthorModel import Author
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from website.models.__init__ import ROLE_CHOICE, SOCIAL_MEDIA, ACADEMIC_LEVEL
from django.contrib.auth.models import User

def view_author_page(request, author_url_slug):
    author = get_object_or_404(Author, author_url_slug=author_url_slug)
    context = {
        'author': author.user,
        'author_connected': False,
        'social_media_index': SOCIAL_MEDIA,
        'graduations_level': ACADEMIC_LEVEL,
    }
    if request.user != author.user:
        return render(request, template_name='author/author.html', context=context, status=200)
    context['author_connected'] = True
    return render(request, template_name='author/author.html', context=context, status=200)