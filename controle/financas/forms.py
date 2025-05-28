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
        fields = ['tipo', 'valor', 'descricao', 'categoria', 'recorrente', 'frequencia']
        
        widgets = {
            'tipo':       forms.Select(attrs={'class': 'w-full bg-gray-700 text-white p-2 rounded'}),
            'valor':      forms.NumberInput(attrs={'class': 'w-full bg-gray-700 text-white p-2 rounded'}),
            'descricao':  forms.TextInput(attrs={'class': 'w-full bg-gray-700 text-white p-2 rounded'}),
            'categoria':  forms.Select(attrs={'class': 'w-full bg-gray-700 text-white p-2 rounded'}),
            'recorrente': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-500'}),
            'frequencia': forms.Select(attrs={'class': 'w-full bg-gray-700 text-white p-2 rounded'}),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']