from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Transacao, Categoria
from .forms import TransacaoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def adicionar_transacao(request):
    if request.method == 'POST':
        # se o formulário for enviado processa os dados
        form = TransacaoForm(request.POST)

        if form.is_valid():
            # salva a transação, associando ao usuário logado
            transacao = form.save(commit = False)
            transacao.usuario = request.user
            transacao.save()

            # tem que ter o nome lista_transacoes lá na urls.pys
            return redirect('lista_transacoes') # redireciona para lista de transações
        
    else:
        # se não foi enviado, exibe o formulário em branco
        form = TransacaoForm()

    # renderiza o template com o formulário
    return render(request, 'adicionar_transacao.html', {'form': form})

"""se configurar o decorador @login_required na view, o Django vai redirecionar o usuário para a página de login se ele não estiver autenticado, e depois de fazer login, ele será redirecionado para a página que estava tentando acessar (ou para uma página padrão)."""

@login_required # garante que o usuário esteja autenticado
def lista_transacoes(request):
    """Busca todas as transações do usuário e as envia para o template"""

    transacoes = Transacao.objects.filter(usuario = request.user) # filtra apenas as transações do usuário logado

    return render(request, 'controle/lista_transacoes.html', {'transacoes': transacoes})

#def register(request):
#    if request.method == 'POST':
#        form = UserCreationForm(request.POST)
        
#        if form.is_valid():
#            form.save()
#            messages.success(request, 'Conta criada com sucesso!')
#            return redirect('login') #redireciona para a pagina de login após o cadastro
        
#        else:
#            messages.error(request, 'Erro ao criar a conta. Tente novamente.')
    
#    else:
#        form = UserCreationForm()

#    return render(request, 'registration/register.html', {'form': form})

def login_register(request):
    if request.method == 'POST':
        if 'login' in request.POST:  # Usuário clicou em login
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')  # Altere para a página desejada
            else:
                messages.error(request, 'Usuário ou senha inválidos.')

        elif 'register' in request.POST:  # Usuário clicou em registro
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Usuário já existe.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'Conta criada com sucesso! Faça login.')
                return redirect('login')

    return render(request, 'registration/login.html')

def user_logout(request):
    logout(request)

    return redirect('login')  # redireciona para a página de login após o logout

def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Verifica se o usuário já existe
        if User.objects.filter(username=username).exists():
            messages.error(request, "Este nome de usuário já está em uso.")
            return redirect("login")

        # Cria o usuário
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Faz login automaticamente após o registro
        login(request, user)
        return redirect("home")  # Redireciona para a página principal após o registro

    return render(request, "registration/register.html")

