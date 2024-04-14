from website.models.ReaderModel import Reader
from website.models import User
from website.forms import EditReaderForm, UserChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.messages import get_messages

def reader_edit(request):
    reader = get_object_or_404(Reader, user__email=request.user.email)
    form = EditReaderForm(instance=reader)
    user_form = UserChangeForm(instance=request.user)
    send_message = False

    if request.POST:
        print(request.POST)
        username_free = check_user_form(request, reader)
        reader_request_post = check_request_post(request)
        if reader_request_post is not None:
            if reader.image != '' and reader_request_post['image'] is not None:
                reader.image.delete(save=True)
                reader.image = reader_request_post['image']
        if username_free and check_reader_form(request, reader):
            messages.success(request, 'Dados atualizados com sucesso.')
            return redirect('/')
        elif not reader_request_post['check_username_request']:
            messages.error(request, 'Nome de usuário já está em uso.')
    context = {
        'userForm': user_form,
        'readerForm': form,
    }
    return render(request, template_name='edit-reader/edit-reader.html', context=context)

def check_request_post(request):
    reader_post_request_data = None
    if request.POST:
        reader_post_request_data = {
            "username": request.POST['username'],
            "name": request.POST['reader_name'],
            "check_username_request": Reader.objects.filter(user__username=request.POST['username']).exclude(user__id=request.user.id).first(),
            "image": request.FILES.get('image', None),
        }

    return reader_post_request_data

def check_user_form(request, reader):
    user_form = UserChangeForm(request.POST, instance=request.user)
    reader_user = check_request_post(request)
    username_free = reader_user['check_username_request'] != reader.user.username
    print("\n\nUserChangeForm IS VALID ==> ", user_form.is_valid())
    if user_form.is_valid() and reader_user['username'] != reader.user.username and username_free:
        user_reader = get_object_or_404(User, id=reader.user.id)
        user_reader.username = reader_user['username']
        user_reader.save()
    return username_free

def check_reader_form(request, reader):
    reader_form = EditReaderForm(request.POST, request.FILES, instance=reader)
    check_post = check_request_post(request)
    if reader_form.is_valid():
        reader.reader_name = check_post['name']
        reader.save()
        return True
    return False
