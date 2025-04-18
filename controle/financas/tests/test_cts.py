import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from financas.models import Transacao, Categoria
from decimal import Decimal

@pytest.fixture
def user(client):
    # cria usuário e já faz login
    u = User.objects.create_user(
        username='usuario1',
        email='usuario1@test.com',
        password='Senha123!'
    )

    client.post(reverse('login'), {'email': u.email, 'password': 'Senha123!'})
    return u

@pytest.fixture
def categoria():
    return Categoria.objects.create(nome='Alimentação')

@pytest.mark.django_db
class TestTransacao:

    def test_ct3_registro_despesa_valida(self, client, user, categoria):
        """
        CT3: Inserir despesa válida (valor 50, categoria Alimentação).
        Deve salvar e redirecionar, e aparecer na lista de transações.
        """

        client.force_login(user)

        url = reverse('adicionar_transacao')
        dados = {
            'descricao': 'Compra mercado',
            'valor': '50',
            'categoria': categoria.id,
            'tipo': 'D',          
            'data': '2025-01-01', 
        }
        resp = client.post(url, dados)
        # redireciona
        assert resp.url == reverse('lista_transacoes')

        # transação existe no banco
        t = Transacao.objects.filter(
            usuario=user,
            descricao='Compra mercado',
            valor=Decimal('50.00'),
            categoria=categoria
        )
        assert t.exists()

        # e ao buscar a lista, vê o item no HTML
        lista = client.get(reverse('lista_transacoes'))
        assert 'Compra mercado' in lista.content.decode()


    def test_ct4_valor_nao_numerico(self, client, user, categoria):
        """
        CT4: Inserir valor não numérico (“abc”). Deve falhar e recusar a entrada.
        """
        url = reverse('adicionar_transacao')
        dados = {
            'descricao': 'Teste inválido',
            'valor': 'abc',
            'categoria': categoria.id,
            'tipo': 'D',
            'data': '2025-01-01',
        }
        resp = client.post(url, dados)

        # não deve ter sido criado
        assert not Transacao.objects.filter(descricao = 'Teste inválido').exists()

        # e o form no contexto deve conter erro em 'valor'
        form = resp.context['form']
        assert 'valor' in form.errors
        assert form.errors['valor'] # pelo menos uma mensagem de erro


@pytest.mark.django_db
def test_ct5_login_usuario(client):
    """
    CT5: Login com dados válidos. Deve autenticar e mostrar mensagem de sucesso.
    """
    u = User.objects.create_user(
        username = 'usuario-login',
        email = 'login@test.com',
        password = 'SenhaLogin1!'
    )

    url = reverse('login')
    resp = client.post(url, {'username': u.username, 'password': 'SenhaLogin1!'})

    # na próxima requisição, o client já está autenticado
    home = client.get(reverse('home'))
    assert home.wsgi_request.user.is_authenticated
