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
    send_message = False
    
    if request.POST:
        print(request.POST)
        social_forms = []
        for social in author_social_media:
            social_forms.append(SocialMediaForm(request.POST, instance=social))
        author_request_post = check_request_post(request)

        if author_request_post is not None:
            if author.image != '' and author_request_post['image'] is not None:
                author.image.delete(save=True)
                author.image = author_request_post['image']
        
        if check_author_form(request, author):
            if update_social_media(request, author_social_media):
                print("REACHING UPDATE: ", "\n")
                send_message = True
            if author_request_post['new_social_addition'] and not any(author_request_post['exclude_social_media']):
                print("REACHING CREATE: ", author_request_post['new_social_addition'], "\n")
                create_social_media(request, author_request_post)
                send_message = True
            if any(author_request_post['exclude_social_media']):
                print("REACHING EXCLUDE AND CHECK ANY: ", any(author_request_post['exclude_social_media']), "\n", author_request_post['exclude_social_media'], "\n")
                exclude_social_media(request, author)
                send_message = True
            if send_message:
                messages.success(request, 'Dados atualizados com sucesso.')
            return redirect('author', slug=author.author_url_slug)
        elif not author_request_post['check_username_request']:
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
        print("CHECK REQUEST FUNCTION | LEN AUTHOR: ", len(Author.objects.get(user__username=request.POST['username']).social_media.all()), "\n")
        print("CHECK REQUEST FUNCTION | LEN REQUEST SOCIAL MEDIA PROFILE", len(request.POST.getlist('social_media_profile')), "\n")
        author_post_request_data = {
            "username": request.POST['username'],
            "name": request.POST['author_name'],
            "check_username_request": Author.objects.filter(user__username=request.POST['username']).exclude(user__id=request.user.id).first(),
            "image": request.FILES.get('image', None),
            "new_social_addition": len(request.POST.getlist('social_media_profile')) > len(Author.objects.get(user__username=request.POST['username']).social_media.all()),
            "exclude_social_media": request.POST.getlist('exclude-social'),
        }
    print("PRINTING AUTHOR POST REQUEST: ", author_post_request_data, "\n")
    return author_post_request_data

def check_user_form(request, author):
    user_form = UserForm(request.POST, instance=request.user)
    author_user = check_request_post(request)
    username_free = author_user['check_username_request'] != author.user.username
    print("Author USER REQUEST: ", author_user['check_username_request'], "\n")
    print("SAVED AUTHOR USERNAME: ", author.user.username, "\n")
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
    print("UPDATE: ", social_media_request_post)
    updated = False
    for i in range(len(author_social_media)):
        if (author_social_media[i].social_media != int(social_media_request_post[i][0])) or (author_social_media[i].social_media_profile != social_media_request_post[i][1]):
            author_social_media[i].social_media = social_media_request_post[i][0]
            author_social_media[i].social_media_profile = social_media_request_post[i][1]
            author_social_media[i].save()
            updated = True
    print(updated)
    return updated

def create_social_media(request, author_request_post):
    social_media_request_post = list(zip(request.POST.getlist('social_media'), request.POST.getlist('social_media_profile')))
    print("CREATE: ", social_media_request_post, "\n")
    author = Author.objects.get(user__username=author_request_post['username'])
    social = author.social_media.all()

    for i in range(len(social), len(social_media_request_post)):
        new_social = SocialMedia.objects.create(
            user_social_media=author,
            social_media=social_media_request_post[i][0],
            social_media_profile=social_media_request_post[i][1],
        )
        new_social.save()
        author.social_media.add(new_social)
            
def exclude_social_media(request, author):
    exclusions = check_request_post(request)['exclude_social_media']
    for exclude_request in exclusions:
        if exclude_request != '':
            social_media = author.social_media.get(social_media=exclude_request).delete()
