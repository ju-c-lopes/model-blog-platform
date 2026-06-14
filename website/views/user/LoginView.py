from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from website.forms.user.LoginForm import LoginForm
from website.models.user.UserModel import User


def _mask_email(email):
    try:
        cut_at_email = email.index("@")
        email_cutted = email[cut_at_email : cut_at_email + 2]
        if email.endswith("br"):
            return f"email {email[:3]}___{email_cutted}__.com.br"
        return f"email {email[:3]}___{email_cutted}__.com"
    except (ValueError, AttributeError):
        return "Email não encontrado."


def _resolve_user_by_identifier(identifier):
    identifier = identifier.strip()
    if "@" in identifier:
        return User.objects.filter(email__iexact=identifier).first()
    return User.objects.filter(username__iexact=identifier).first()


def _login_context(form, remember=False, email_not_found=False):
    context = {"form": form, "remember": remember}
    if email_not_found:
        context["email_not_found"] = email_not_found
    return context


def login_user(request):
    remember = request.POST.get("remember")
    user_to_remember = (request.POST.get("nome") or "").strip()

    if request.POST and remember:
        if user_to_remember:
            user = User.objects.filter(username__iexact=user_to_remember).first()
            if user:
                messages.success(request, f"Seu email é: {_mask_email(user.email)}")
            else:
                messages.error(request, f"Usuário «{user_to_remember}» não encontrado.")
            return render(
                request,
                "blog/pages/login/login.html",
                context=_login_context(LoginForm()),
            )
        return render(
            request,
            "blog/pages/login/login.html",
            context=_login_context(LoginForm(), remember=True),
        )

    email_not_found = False

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data["identifier"]
            password = form.cleaned_data.get("password") or ""
            user = _resolve_user_by_identifier(identifier)
            if user is None:
                if "@" in identifier:
                    messages.error(request, f"{_mask_email(identifier)} não encontrado.")
                else:
                    messages.error(request, f"Usuário «{identifier}» não encontrado.")
                email_not_found = True
            elif not password:
                messages.error(request, "Informe a senha.")
            else:
                authenticated = authenticate(request, email=user.email, password=password)
                if authenticated is not None:
                    login(request, authenticated)
                    return redirect("/")
                messages.error(request, "Senha inválida.")
        else:
            messages.error(request, "Preencha o formulário corretamente.")
    else:
        form = LoginForm()

    return render(
        request,
        "blog/pages/login/login.html",
        context=_login_context(form, email_not_found=email_not_found),
    )
