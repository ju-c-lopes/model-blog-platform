from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.urls import reverse
from website.models import User, Author, Reader
from website.forms import UserCreationForm
from django.contrib import messages
from django.contrib.messages import get_messages

def sign_up_user(request):
    user_form = UserCreationForm()
    print(request.POST)
    if request.POST:
        user_form = UserCreationForm(request.POST)
        cont = len(User.objects.all()) + 1
        
        treated_username = request.POST.get("nome", None).split(" ")[0].lower() + f"-user{cont}"
        
        password1 = request.POST.get("password1", None)
        password2 = request.POST.get("password2", None)
        is_staff = True if request.POST.get("tipo-user") == "author" else False
        
        print(request.POST.get("phone"))
        
        if password1 == password2:
            user = User.objects.create_user(
                username = treated_username,
                email = request.POST.get("email", None),
                phone_number = request.POST.get("phone", None),
                password = request.POST.get('password2', None),
                is_staff = is_staff,
            )
            
            type_user_created = create_author(request, user) if request.POST.get("tipo-user") == "author" else create_reader(request, user)
            messages.success(request, f"O usuário {user.username} foi registrado com sucesso.")
            print("\nDefinido messages \n")
            return redirect("login")
        else:
            #print(messages.get_messages(request))
            messages.error(request, "A senha digitada não confere.")
            
    context ={
        "form": user_form,
    }
    return render(request, template_name="sign-up/sign-up.html", context=context, status=200)


def create_author(request, user):
    author_name = request.POST.get("nome", None)
    slug = str()
    for n in author_name.split(" "):
        if n == author_name.split(" ")[-1]:
            slug += n.lower()
        else:
            slug += f"{n.lower()}-"
    
    author = Author(
       user = user,
       author_name = author_name,
       author_url_slug = slug,
       access_level = 1,
    )
    author.save()
    return author


def create_reader(request, user):
    reader_name = request.POST.get("nome", None)
    reader = Reader(
        user = user,
        reader_name = reader_name,
        access_level = 2,
    )
    reader.save()
    return reader
