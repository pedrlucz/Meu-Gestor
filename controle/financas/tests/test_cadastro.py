import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.mark.django_db  # Marca os testes que precisam acessar o banco de dados
class TestCadastroUsuario:
    
    def test_cadastro_valido(self, client):
        """
        CT1: Testa cadastro com dados válidos
        """
        # define a URL para a view de registro
        url = reverse('register')
        
        # prepara os dados de teste
        dados = {
            'username': 'Usuario Teste',
            'email': 'teste@exemplo.com',
            'password': 'Senha123!',
            'confirm_password': 'Senha123!' 
        }
        
        # simula uma requisição POST para a view de registro
        response = client.post(url, dados)
        
        # verifica se o usuário foi criado no banco de dados
        assert User.objects.filter(email='teste@exemplo.com').exists()
        
        # verifica se a resposta redireciona (comum após um registro bem-sucedido)
        assert response.status_code == 302
        
        # depois eu preciso ver de alternativa: se exibe uma mensagem na página, verificar o conteúdo
        # response = client.post(url, dados, follow=True)  # follow=True segue redirecionamentos
        # assert 'Usuário cadastrado com sucesso' in response.content.decode()
    
    def test_cadastro_email_vazio(self, client):
        """
        CT2: Testa cadastro com email vazio
        """
        url = reverse('register')
        
        dados = {
            'username': 'Usuario Teste',
            'email': '',
            'password': 'Senha123!',
            'confirm_password': 'Senha123!'
        }
        
        response = client.post(url, dados)
        
        # verifica se o usuário NÃO foi criado
        assert not User.objects.filter(username='Usuario Teste').exists()
        
        # verifica se a página retorna com código 302 (com redirecionamento)
        assert response.status_code == 302

        # verifica o redirecionamento para a página de registro
        assert response.url == reverse('register')

        # acessa novamente a página de cadastro (após redirecionamento)
        response = client.get(reverse('register'))
        
        # verifica se há mensagem de erro no conteúdo da página
        assert 'Erro de validação' in response.content.decode() or \
               'Este campo é obrigatório' in response.content.decode()