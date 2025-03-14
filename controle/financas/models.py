from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nome = models.CharField(max_length = 100)

    def __str__(self):
        return self.nome

class Transacao(models.Model):

    TIPO_CHOICES = [
                        ('R', 'Receita'),
                        ('D', 'Despesa')
                                            ]

    usuario = models.ForeignKey(User, on_delete = models.CASCADE)
    tipo = models.CharField(max_length = 1, choices = TIPO_CHOICES)
    valor = models.DecimalField(max_digits = 10, decimal_places = 2)
    descricao = models.CharField(max_length = 200)
    categoria = models.ForeignKey(Categoria, on_delete = models.SET_NULL, null = True)
    data = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'{self.get_tipo_display() - {self.descricao}}'