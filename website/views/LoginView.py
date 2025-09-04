from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect, render

from website.forms.LoginForm import LoginForm
from website.models import Author, User


def login_user(request):
    context = None
    email_not_found = False

    remember = request.POST.get("remember", False)
    user_to_remember = request.POST.get("nome", False)
    nome = None

    # Caso o usuário indique um nome para remember
    if remember and user_to_remember:
        try:
            # Tentará encontrar o usuário pelo nome
            user_to_remember = user_to_remember.strip()
            nome = Author.objects.filter(nome__contains=user_to_remember)
            remember = False
        except Exception:
            nome = user_to_remember

    if request.POST:
        form = LoginForm(request.POST)
        print(request)
        if form.is_valid():
            email = request.POST.get("email")
            password = request.POST.get("password")
            try:
                user_login = User.objects.get(email=email)
                pass_user = check_password(password, user_login.password)
                user = authenticate(email=email, password=password)
                if user is not None and pass_user:
                    login(request, user)
                    return redirect("/")
                else:
                    messages.error(request, "Senha inválida.")

            except Exception:
                # Be defensive: if email is malformed or missing '@',
                # fallback to a simple message
                try:
                    cut_at_email = email.index("@")
                    email_cutted = email[cut_at_email : cut_at_email + 2]
                    if email.endswith("br"):
                        masked_email = f"email {email[:3]}___{email_cutted}__.com.br"
                    else:
                        masked_email = f"email {email[:3]}___{email_cutted}__.com"
                    masked_email += " não encontrado."
                except Exception:
                    masked_email = "Email não encontrado."
                messages.error(request, masked_email)
                email_not_found = True

        else:
            messages.error(request, "Preencha o formulário corretamente.")
    else:
        form = LoginForm()

    context = {
        "form": form,
        "usuario": request.GET.get("usuario", None) if nome is None else nome,
        "remember": remember,
        "nome": nome,
    }

    if email_not_found:
        context["email_not_found"] = email_not_found

    return render(request, "login/login.html", context=context, status=200)
