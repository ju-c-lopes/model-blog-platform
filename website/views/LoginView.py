from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login


def login_user(request):
    context = None

    # Message verifica se usuário foi cadastrado com sucesso, senão
    # somente é iniciada como None
    message = {
        'type': request.GET.get('type', None),
        'text': request.GET.get('message', None),
        'usuario_inv': False,
    }

    """lembrar = request.POST.get('lembrar', False)
    nome_a_recordar = request.POST.get('nome', False)
    nome = None"""

    # Caso o usuário indique um nome para lembrar
    """if lembrar and nome_a_recordar:
        try:
            # Tentará encontrar o usuário pelo nome
            nome_a_recordar = nome_a_recordar.strip()
            nome = Usuario.objects.filter(nome__contains=nome_a_recordar)
            lembrar = False
            message['type'] = 'success'
        except:
            # se não houver usuário com este nome enviará mensagem de não encontrado
            nome = nome_a_recordar
            message['text'] = f"Nome {nome} não encontrado."
            message['type'] = 'erro'
            message['usuario_inv'] = True"""

    #el
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            try:
                usuario = Usuario.objects.get(user__username=username)
                pass_user = check_password(password, usuario.user.password)
                user = authenticate(username=username, password=password)
                if user is not None and pass_user:
                    login(request, user)
                    return redirect('/')
                else:
                    message['text'] = f"Senha inválida."
                    message['type'] = 'erro'
            except:
                message['text'] = f"Usuário {username} não existe."
                message['type'] = 'erro'
                message['usuario_inv'] = True
        else:
            message['text'] = "Preencha o formulário corretamente."
            message['type'] = 'erro'
    else:
        form = LoginForm()
    
    context = {
        'usuario': request.GET.get('usuario', None) if nome is None else nome,
        'message': message,
        'lembrar': lembrar,
        'nome': nome,
    }

    if message['usuario_inv'] and lembrar:
        url = reverse('login') + f"?usuario={context['nome']}&message={context['message']['text']}&type={context['message']['type']}"
        return redirect(url)
    return render(request, 'login/login.html', context=context, status=200)