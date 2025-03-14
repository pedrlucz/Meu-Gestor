from django.urls import path
from .views import adicionar_transacao, lista_transacoes, home, login_register, user_logout, register_user
from . import views

urlpatterns = [
    path('adicionar/', adicionar_transacao, name = 'adicionar_transacao'),
    path('transacoes/' , lista_transacoes, name = 'lista_transacoes'),
    path('register/', register_user, name = 'register'),
    path('login/', login_register, name = 'login'),
    path('logout/', user_logout, {'next_page':'login'}, name = 'logout'),
    path('', home, name = 'home')
]