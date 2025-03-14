from django import forms
from .models import Transacao, Categoria

class TransacaoForm(forms.ModelForm):
    # para adicionar um campo de seleção para categorias
    categoria = forms.ModelChoiceField(queryset = Categoria.objects.all() , empty_label = 'Selecione uma categoria')

    # pra validar o valor
    def clean_valor(self):
        valor = self.cleaned_data['valor']

        if valor <= 0 :
            raise forms.ValidationError('O valor deve ser maior que zero')
        
        return valor

    class Meta:
        model = Transacao
        fields = ['tipo', 'valor', 'descricao', 'categoria']