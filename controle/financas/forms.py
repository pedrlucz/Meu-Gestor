from django import forms
from .models import Transacao, Categoria

class TransacaoForm(forms.ModelForm): # modelform cria automaticamente um formulário com os campos definidos
    # para adicionar um campo de seleção para categorias (modelchoicefield)
    categoria = forms.ModelChoiceField(queryset = Categoria.objects.all() , empty_label = 'Selecione uma categoria')

    # pra validar o valor (clean <nome_de_algo>)
    def clean_valor(self):
        # recupera o valor passado pelo usuário
        valor = self.cleaned_data['valor']

        if valor <= 0 :
            raise forms.ValidationError('O valor deve ser maior que zero')
        
        return valor

    # é usada para definir configurações do ModelForm
    class Meta:
        # ta ligado à transação
        model = Transacao
        fields = ['tipo', 'valor', 'descricao', 'categoria']