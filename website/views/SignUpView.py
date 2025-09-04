import re
import unicodedata

from django.contrib import messages
from django.shortcuts import redirect, render

from website.forms import UserCreationForm
from website.models import Author, Reader, User


def sign_up_user(request):
    user_form = UserCreationForm()
    if request.POST:
        user_form = UserCreationForm(request.POST)
        cont = len(User.objects.all()) + 1

        request_name = treat_accentuation(request.POST.get("nome", None))

        treated_username = request_name.split(" ")[0].lower() + f"-user{cont}"

        password1 = request.POST.get("password1", None)
        password2 = request.POST.get("password2", None)
        is_staff = True if request.POST.get("tipo-user") == "author" else False

        if check_password_request(password1, password2):
            user = User.objects.create_user(
                username=treated_username,
                email=request.POST.get("email", None),
                phone_number=request.POST.get("phone", None),
                password=request.POST.get("password2", None),
                is_staff=is_staff,
            )

            if user.is_staff:
                create_author(request, user)
            else:
                create_reader(request, user)
            messages.success(
                request, f"O usuário {user.username} foi registrado com sucesso."
            )
            return redirect("login")
        else:
            messages.error(request, "A senha digitada não confere.")

    context = {
        "form": user_form,
    }
    return render(
        request, template_name="sign-up/sign-up.html", context=context, status=200
    )


def create_author(request, user):
    author_name = request.POST.get("nome", None)
    author_name_replaced = treat_accentuation(author_name)

    slug = str()
    for n in author_name_replaced.split(" "):
        if n == author_name_replaced.split(" ")[-1]:
            slug += n.lower()
        else:
            slug += f"{n.lower()}-"

    author = Author(
        user=user,
        author_name=author_name,
        author_url_slug=slug,
        access_level=1,
    )
    author.save()
    return author


def create_reader(request, user):
    reader_name = request.POST.get("nome", None)
    reader = Reader(
        user=user,
        reader_name=reader_name,
        access_level=2,
    )
    reader.save()
    return reader


def treat_accentuation(request_name):
    replace_accentuation = unicodedata.normalize("NFD", request_name)
    replace_accentuation = replace_accentuation.encode("ascii", "ignore")
    author_name_replaced = replace_accentuation.decode("utf-8")
    return author_name_replaced


def check_password_request(pass1, pass2):
    validations = [pass1 == pass2]
    validations.append(len(pass2) >= 10 and len(pass2) <= 16)
    upper_regex = re.compile(r"[A-Z]").search(pass2)
    validations.append(upper_regex)
    number_regex = re.compile(r"\d").search(pass2)
    validations.append(number_regex)
    special_regex = re.compile(r"[\W_]").search(pass2)
    validations.append(special_regex)
    return all(validations)
