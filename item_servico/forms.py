from django import forms
from .models import ItemServico


class ItemServicoForm(forms.ModelForm):
    """Formulário para o modelo ItemServico."""
    
    class Meta:
        model = ItemServico
        fields = ['nome', 'descricao', 'quantidade', 'preco_unitario']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do item/serviço'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição detalhada do item/serviço'
            }),
            'quantidade': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quantidade disponível',
                'min': '0'
            }),
            'preco_unitario': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
        }
        labels = {
            'nome': 'Nome do Item/Serviço',
            'descricao': 'Descrição',
            'quantidade': 'Quantidade em Estoque',
            'preco_unitario': 'Preço Unitário (R$)',
        }
        
    def clean_preco_unitario(self):
        """Validação personalizada para preço unitário."""
        preco = self.cleaned_data.get('preco_unitario')
        if preco is not None and preco < 0:
            raise forms.ValidationError('O preço não pode ser negativo.')
        return preco
        
    def clean_quantidade(self):
        """Validação personalizada para quantidade."""
        quantidade = self.cleaned_data.get('quantidade')
        if quantidade is not None and quantidade < 0:
            raise forms.ValidationError('A quantidade não pode ser negativa.')
        return quantidade

