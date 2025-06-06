from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nome = models.CharField(max_length = 100)
    usuario = models.ForeignKey(User, on_delete = models.CASCADE)

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
    categoria = models.ForeignKey(Categoria, on_delete = models.SET_NULL, null = True, blank = True)
    data = models.DateTimeField(auto_now_add = True)

    recorrente = models.BooleanField(default=False)
    frequencia = models.CharField(
        max_length=20,
        choices=(('mensal','Mensal'),('semanal','Semanal'),('anual','Anual')),
        default='mensal'
    )

    def __str__(self):
        return f'{self.get_tipo_display() - {self.descricao}}'