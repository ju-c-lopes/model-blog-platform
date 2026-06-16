from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from website.forms.user.LoginForm import LoginForm
from website.models.user.UserModel import User

REMEMBER_MODE_USERNAME = "username"
REMEMBER_MODE_EMAIL = "email"


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


def _login_context(form, remember=False, remember_mode=None):
    context = {"form": form, "remember": remember}
    if remember_mode:
        context["remember_mode"] = remember_mode
    return context


def login_user(request):
    remember = request.POST.get("remember")
    remember_mode = request.POST.get("remember_mode")
    recovery_value = (request.POST.get("recovery_value") or "").strip()

    if request.POST and remember:
        if recovery_value:
            if remember_mode == REMEMBER_MODE_EMAIL:
                user = User.objects.filter(email__iexact=recovery_value).first()
                if user:
                    messages.success(request, f"Seu usuário é: {user.username}")
                else:
                    messages.error(request, f"Email «{recovery_value}» não encontrado.")
            else:
                user = User.objects.filter(username__iexact=recovery_value).first()
                if user:
                    messages.success(request, f"Seu email é: {_mask_email(user.email)}")
                else:
                    messages.error(request, f"Usuário «{recovery_value}» não encontrado.")
            return render(
                request,
                "blog/pages/login/login.html",
                context=_login_context(LoginForm()),
            )
        if remember_mode in (REMEMBER_MODE_USERNAME, REMEMBER_MODE_EMAIL):
            return render(
                request,
                "blog/pages/login/login.html",
                context=_login_context(LoginForm(), remember=True, remember_mode=remember_mode),
            )

    remember_mode = None

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data["identifier"]
            password = form.cleaned_data.get("password") or ""
            user = _resolve_user_by_identifier(identifier)
            if user is None:
                if "@" in identifier:
                    messages.error(request, f"{_mask_email(identifier)} não encontrado.")
                    remember_mode = REMEMBER_MODE_USERNAME
                else:
                    messages.error(request, f"Usuário «{identifier}» não encontrado.")
                    remember_mode = REMEMBER_MODE_EMAIL
            elif not password:
                messages.error(request, "Informe a senha.")
            else:
                authenticated = authenticate(request, email=user.email, password=password)
                if authenticated is not None:
                    backend = getattr(
                        authenticated,
                        "backend",
                        "django.contrib.auth.backends.ModelBackend",
                    )
                    login(request, authenticated, backend=backend)
                    return redirect("/")
                messages.error(request, "Senha inválida.")
        else:
            messages.error(request, "Preencha o formulário corretamente.")
    else:
        form = LoginForm()

    return render(
        request,
        "blog/pages/login/login.html",
        context=_login_context(form, remember_mode=remember_mode),
    )
