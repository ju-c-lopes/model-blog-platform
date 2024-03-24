from website.models.AuthorModel import Author
from website.models.AuthorSocialMediaModel import SocialMedia
from django.contrib.auth.models import User
from website.forms.EditAuthorForm import EditAuthorForm, UserForm, SocialMediaForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from website.models.__init__ import ROLE_CHOICE, SOCIAL_MEDIA, ACADEMIC_LEVEL
from django.contrib import messages
from django.contrib.messages import get_messages

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
    author = get_object_or_404(Author, author_url_slug=slug)
    user_author = get_object_or_404(User, id=author.user.id)
    author_social_media = author.social_media.all()
    form = EditAuthorForm(instance=author)
    user_form = UserForm(instance=request.user)
    social_forms = []
    for social in author_social_media:
        social_forms.append(SocialMediaForm(instance=social))
    social_empty_form = SocialMediaForm()
    username_free = True
    
    if request.POST:
        form = EditAuthorForm(request.POST, request.FILES, instance=author)
        user_form = UserForm(request.POST, instance=request.user)
        social_forms = []
        for social in author_social_media:
            social_forms.append(SocialMediaForm(request.POST, instance=social))
        author_request_post = check_request_post(request)
        username_free = author_request_post['check_username_request'] is None

        if author_request_post is not None:
            if author.image != '' and author_request_post['image'] is not None:
                print(author.image, "authooor image")
                author.image.delete(save=True)
            author_request_post['image']
        if form.is_valid() and user_form.is_valid():
            author.image = author_request_post['image']
            if author_request_post['username'] != author.user.username and username_free:
                author.user.username = author_request_post['username']
                user_author.save()
            author.save()
            messages.success(request, 'Dados atualizados com sucesso.')
            return redirect('author', slug=author.author_url_slug)
        elif not username_free:
            messages.error(request, 'Nome de usuário já está em uso.')
    context = {
        'socialEmptyForm': social_empty_form,
        'userForm': user_form,
        'authorForm': form,
        'socialForms': social_forms,
    }
    return render(request, template_name='edit-author/edit-author.html', context=context)

def check_request_post(request):
    author_post_request_data = None
    if request.POST:
        author_post_request_data = {
            "username": request.POST['username'],
            "name": request.POST['author_name'],
            "check_username_request": Author.objects.filter(user__username=request.POST['username']).exclude(user__id=request.user.id).first(),
            "image": request.FILES.get('image', None),
        }
    return author_post_request_data

