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
    author = get_object_or_404(Author, author_url_slug=slug)
    author_social_media = author.social_media.all()
    form = EditAuthorForm(instance=author)
    user_form = UserForm(instance=request.user)
    social_forms = []
    for social in author_social_media:
        social_forms.append(SocialMediaForm(instance=social))
    social_empty_form = SocialMediaForm()
    username_free = True
    
    if request.POST:
        social_forms = []
        for social in author_social_media:
            social_forms.append(SocialMediaForm(request.POST, instance=social))
        author_request_post = check_request_post(request)

        if author_request_post is not None:
            if author.image != '' and author_request_post['image'] is not None:
                author.image.delete(save=True)
                author.image = author_request_post['image']
        username_free = check_user_form(request, author)
        if check_author_form(request, author) and username_free:
            create_social_media(request, author)
            
            author_social_media = author.social_media.all()
            update_social_media(request, author_social_media)
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

def check_user_form(request, author):
    user_form = UserForm(request.POST, instance=request.user)
    author_user = check_request_post(request)
    username_free = author_user['check_username_request'] is None
    if user_form.is_valid() and author_user['username'] != author.user.username and username_free:
        user_author = get_object_or_404(User, id=author.user.id)
        user_author.username = author_user['username']
        user_author.save()
    return username_free

def check_author_form(request, author):
    author_form = EditAuthorForm(request.POST, request.FILES, instance=author)
    check_post = check_request_post(request)
    if author_form.is_valid():
        author.author_name = check_post['name']
        author.save()
        return True
    return False

def update_social_media(request, author_social_media):
    social_media_request_post = list(zip(request.POST.getlist('social_media'), request.POST.getlist('social_media_profile')))
    print("AUTHOR SOCIAL MEDIAS: ", author_social_media, " requesf ", social_media_request_post)
    for i in range(len(SOCIAL_MEDIA)):
        if i == len(author_social_media):
            break        
        if (author_social_media[i].social_media != social_media_request_post[i][0]) or (author_social_media[i].social_media_profile != social_media_request_post[i][1]):
            author_social_media[i].social_media = social_media_request_post[i][0]
            author_social_media[i].social_media_profile = social_media_request_post[i][1]
            author_social_media[i].save()

def create_social_media(request, author):
    social_media_request_post = list(zip(request.POST.getlist('social_media'), request.POST.getlist('social_media_profile')))
    social = author.social_media.all()
    if social_media_request_post[len(social)][1] == '':
        print("SKIPPING...")
        return
    print(social)
    for i in range(len(social), len(SOCIAL_MEDIA)):
        if social_media_request_post[i][1] != '':
            new_social = SocialMedia.objects.create(
                user_social_media=author,
                social_media=social_media_request_post[i][0],
                social_media_profile=social_media_request_post[i][1],
            )
            new_social.save()
            author.social_media.add(new_social)
            
