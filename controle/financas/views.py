from django.contrib.auth import authenticate, login, logout # verifica se as credenciais tão corretas, se sim o login cria o lgin e o logout...
from django.contrib.auth.decorators import login_required # garante que só usuários autenticados vão conseguir entrar
from django.db.models.functions import TruncMonth
from .forms import TransacaoForm, CategoriaForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User # que guarda informação, como nome, email, senha
from django.contrib import messages
from django.db.models import Sum
from .models import Transacao

# from django.http import HttpResponseRedirect
# from django.urls import reverse

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
            return redirect('lista_transacoes') # redireciona o usuário para a pag lista de transações
        
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

    return render(request, 'lista_transacoes.html', {'transacoes': transacoes})

def login_register(request):
    if request.method == 'POST':
        # 1) Pega email e senha do formulário
        email    = request.POST.get('email')
        password = request.POST.get('password')

        # 2) Busca usuário pelo email
        try:
            user_obj = User.objects.get(email = email)
        except User.DoesNotExist:
            user_obj = None

        # 3) Se achou, autentica com o username real; senão, pula pra None
        if user_obj:
            user = authenticate(request,
                                username = user_obj.username,
                                password = password)
        else:
            user = None

        # 4) Se autenticou, faz login e redireciona
        if user is not None:
            login(request, user)
            return redirect('dashboard')

        # 5) Senão, erro e volta pro form de login
        messages.error(request, "Usuário ou senha inválidos.")
        return redirect('login')

    # método GET — só renderiza o form
    return render(request, 'registration/login.html')

# quando fizer o html do logout chamar aqui
def user_logout(request):
    logout(request)

    return redirect('home')  # redireciona para a página de home após o logout

def register_user(request):
    if request.method == "POST":
        # pega dados e já tira espaços extras
        username         = request.POST.get("username", "").strip()
        email            = request.POST.get("email", "").strip()
        password         = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        # validações básicas de presença
        if not username:
            messages.error(request, "O nome de usuário é obrigatório.")
            return redirect("register")

        if not email:
            messages.error(request, "Este campo é obrigatório.")
            return redirect("register")

        if not password:
            messages.error(request, "A senha é obrigatória.")
            return redirect("register")

        if password != confirm_password:
            messages.error(request, "As senhas não conferem.")
            return redirect("register")

        # valida se já existe username ou email
        if User.objects.filter(username = username).exists():
            messages.error(request, "Este nome de usuário já está em uso.")
            return redirect("register")

        if User.objects.filter(email = email).exists():
            messages.error(request, "Este email já está cadastrado.")
            return redirect("register")

        # tudo ok, cria e faz login
        user = User.objects.create_user(
                                            username = username,
                                                email = email,
                                                    password = password
                                                                            )
        user.save()
        login(request, user)
        # next_url = request.GET.get('next', 'home')
        # messages.success(request, "Conta criada com sucesso! Bem-vindo(a).")
        return redirect('dashboard')

    return render(request, "registration/register.html")

@login_required
def dashboard(request):
    # soma total de receitas e despesas do usuário
    total_receitas = Transacao.objects.filter(usuario = request.user, tipo = 'R') \
        .aggregate(Sum('valor'))['valor__sum'] or 0
    
    total_despesas = Transacao.objects.filter(usuario = request.user, tipo = 'D') \
        .aggregate(Sum('valor'))['valor__sum'] or 0
    
    resultado = total_receitas - total_despesas

    # vai ser a série mensal de receitas (para o gráfico)
    series = (
                    Transacao.objects.filter(usuario = request.user, tipo = 'R')
                    .annotate(mes = TruncMonth('data'))
                    .values('mes')
                    .annotate(total = Sum('valor'))
                    .order_by('mes')
                                                                                    )

    series_despesas = (
        Transacao.objects.filter(usuario = request.user, tipo = 'D')
        .annotate(mes = TruncMonth('data'))
        .values('mes')
        .annotate(total = Sum('valor'))
        .order_by('mes')
    )

    meses = [item['mes'].strftime('%b') for item in series]
    valores = [float(item['total']) for item in series]

    # dados mensais
    valores_despesas = [float(item['total']) for item in series_despesas]

    # ajustar resultado mensalmente
    valores_resultado = [
        r - d if i < len(valores_despesas) else r
        for i, (r, d) in enumerate(zip(valores, valores_despesas))
    ]

    context = {
                    'total_receitas': total_receitas,
                        'total_despesas': total_despesas,
                            'meses': meses,
                                'valores': valores,
                                    'resultado': resultado,
                                        'valores_despesas': valores_despesas,
                                            'valores_resultado': valores_resultado
                                                            }

    return render(request, 'dashboard.html', context)

@login_required
def cadastrar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)

        if form.is_valid():
            categoria = form.save(commit = False)
            categoria.usuario = request.user
            categoria.save()
            
            return redirect('adicionar_transacao')
        
    else:
        form = CategoriaForm()

    return render(request, 'categorias/cadastrar.html', {'form': form})