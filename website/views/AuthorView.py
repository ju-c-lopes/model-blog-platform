from website.models.AuthorModel import Author
from website.forms.EditAuthorForm import EditAuthorForm, UserForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from website.models.__init__ import ROLE_CHOICE, SOCIAL_MEDIA, ACADEMIC_LEVEL
from django.contrib.auth.models import User
import os

def view_author_page(request, slug):
    author = get_object_or_404(Author, author_url_slug=slug)
    context = {
        'author': author,
        'author_connected': False,
        'social_media_index': SOCIAL_MEDIA,
        'graduations_level': ACADEMIC_LEVEL,
    }
    if request.user != author.user:
        return render(request, template_name='author/author.html', context=context, status=200)
    context['author_connected'] = True
    return render(request, template_name='author/author.html', context=context, status=200)

def edit_author_profile(request, slug):
    message = None
    username_free = True
    
    author = get_object_or_404(Author, author_url_slug=slug)
    
    form = EditAuthorForm(instance=author)
    user_form = UserForm(instance=request.user)
    
    if request.POST:
        form = EditAuthorForm(request.POST, request.FILES, instance=author)
        user_form = UserForm(request.POST, instance=request.user)
        check_username = Author.objects.filter(user__username=request.POST['username']).exclude(user__id=request.user.id).first()
        print(check_username)
        username_free = check_username is None
        print(username_free)
        
        if form.is_valid() and user_form.is_valid() and username_free and request.POST['username'] is not None:
                author.username = request.POST['username']
        if request.POST['author_name'] is not None:
                author.author_name = request.POST['author_name']
        if request.FILES and request.FILES['image'] is not None:
                author.image = request.FILES['image']
        author.save()
            
        message = {
            'type': 'success',
            'text': 'Dados atualizados com sucesso.',
        }

        url = reverse('author') + f"?message={message['text']}&type={message['type']}"
        return redirect(url)

    else:
        if not username_free:
            message = {
                'type': 'erro',
                'text': 'Nome de usuário já está em uso.'
            }

    context = {
        'message': message,
        'userForm': user_form,
        'authorForm': form,
    }

    return render(request, template_name='edit-author/edit-author.html', context=context)