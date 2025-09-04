from django import forms
from .models import ProdutoEstoque, MovimentacaoEstoque, CategoriaEstoque


class CategoriaEstoqueForm(forms.ModelForm):
    class Meta:
        model = CategoriaEstoque
        fields = '__all__'
        widgets = {
            'cor': forms.TextInput(attrs={'type': 'color'}),
        }


class ProdutoEstoqueForm(forms.ModelForm):
    class Meta:
        model = ProdutoEstoque
        fields = '__all__'
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }


class MovimentacaoEstoqueForm(forms.ModelForm):
    class Meta:
        model = MovimentacaoEstoque
        fields = '__all__'
        widgets = {
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }


