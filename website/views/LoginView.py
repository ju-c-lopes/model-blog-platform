from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login
from website.forms.LoginForm import LoginForm
from website.models import Author
from django.contrib import messages
from django.contrib.messages import get_messages

def login_user(request):
    context = None
    email_not_found = False

    remember = request.POST.get('remember', False)
    user_to_remember = request.POST.get('nome', False)
    nome = None
    print("remember: ", remember, "\n\n")

    # Caso o usuário indique um nome para remember
    if remember and user_to_remember:
        try:
            # Tentará encontrar o usuário pelo nome
            user_to_remember = user_to_remember.strip()
            nome = Author.objects.filter(nome__contains=user_to_remember)
            remember = False
        except:
            nome = user_to_remember

    if request.POST:
        print(request.POST)
        form = LoginForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            try:
                usuario = Author.objects.get(user__email=email)
                pass_user = check_password(password, usuario.user.password)
                user = authenticate(email=email, password=password)
                print("\nUser e Passuser: ===>  ", user is not None and pass_user)
                if user is not None and pass_user:
                    login(request, user)
                    return redirect('/')
                else:
                    messages.error(request, 'Senha inválida.')
                    
            except:
                print("email except ==> ", email,"\n\n")
                cut_at_email = email.index('@')
                print("\nINDEX EMAIL ==> ", cut_at_email)
                email_cutted = email[cut_at_email:cut_at_email+2]
                print("\nCUTTED EMAIL ==> ", email_cutted, "\n")
                masked_email = f'email {email[:3]}___{email_cutted}__.com.br' if email[-2:] == 'br' else f'email {email[:3]}___{email_cutted}__.com'
                masked_email += " não encontrado."
                messages.error(request, masked_email)
                email_not_found = True
                
        else:
            messages.error(request, "Preencha o formulário corretamente.")
    else:
        form = LoginForm()
    
    context = {
        'form': form,
        'usuario': request.GET.get('usuario', None) if nome is None else nome,
        # 'message': message,
        'remember': remember,
        'nome': nome,
    }

    if email_not_found:
        context['email_not_found'] = email_not_found
    print("\nContext ===> ", context, "\n\n")
    
    return render(request, 'login/login.html', context=context, status=200)