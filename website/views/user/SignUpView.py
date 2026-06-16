from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from website.forms.user.UserCreationForm import UserCreationForm
from website.models.user.UserModel import User
from website.services.user.admin_approval import verify_superuser_credentials
from website.services.user.user_registration import (
    create_author_profile,
    create_reader_profile,
    generate_username,
)


def sign_up_user(request):
    user_form = UserCreationForm()
    if not request.POST:
        return _render_signup(request, user_form)

    nome = (request.POST.get("nome") or "").strip()
    email = (request.POST.get("email") or "").strip()
    phone = request.POST.get("phone") or ""
    password1 = request.POST.get("password1") or ""
    password2 = request.POST.get("password2") or ""
    tipo_user = request.POST.get("tipo-user", "reader")
    is_author = tipo_user == "author"
    is_approval_step = request.POST.get("approval") == "1"

    if is_approval_step:
        if not verify_superuser_credentials(
            request.POST.get("super", ""),
            request.POST.get("pass-super", ""),
        ):
            messages.error(request, "Credenciais de administrador inválidas.")
            return _render_signup(
                request,
                user_form,
                aprovar=True,
                signup_data=_signup_data(nome, email, phone, password1, password2, tipo_user),
            )
        return _register_user(request, nome, email, phone, password2, is_author=True)

    try:
        validate_password(password2)
        password_ok = password1 == password2
    except ValidationError:
        password_ok = False

    if not password_ok:
        messages.error(request, "A senha digitada não confere ou não satisfaz as regras.")
        return _render_signup(request, UserCreationForm(request.POST))

    if is_author:
        return _render_signup(
            request,
            UserCreationForm(request.POST),
            aprovar=True,
            signup_data=_signup_data(nome, email, phone, password1, password2, tipo_user),
        )

    return _register_user(request, nome, email, phone, password2, is_author=False)


def _signup_data(nome, email, phone, password1, password2, tipo_user):
    return {
        "nome": nome,
        "email": email,
        "phone": phone,
        "password1": password1,
        "password2": password2,
        "tipo_user": tipo_user,
    }


def _register_user(request, nome, email, phone, password, is_author):
    username = generate_username(nome)
    user = User.objects.create_user(
        username=username,
        email=email,
        phone_number=phone or None,
        password=password,
        is_staff=is_author,
    )
    if is_author:
        create_author_profile(user, nome)
    else:
        create_reader_profile(user, nome)
    messages.success(request, f"O usuário {user.username} foi registrado com sucesso.")
    return redirect("login")


def _render_signup(request, form, aprovar=False, signup_data=None):
    context = {"form": form, "aprovar": aprovar}
    if signup_data:
        context.update(signup_data)
        context["password"] = signup_data.get("password2", "")
    return render(
        request,
        template_name="blog/pages/sign-up/sign-up.html",
        context=context,
        status=200,
    )
