from django import forms
from .models import Financeiro
from pessoa_falecida.models import PessoaFalecida


class FinanceiroForm(forms.ModelForm):
    """Formulário para o modelo Financeiro."""
    
    class Meta:
        model = Financeiro
        fields = ['pessoa_falecida', 'tipo', 'descricao', 'valor', 'data_vencimento', 'status']
        widgets = {
            'pessoa_falecida': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição da transação'
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'data_vencimento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        labels = {
            'pessoa_falecida': 'Pessoa Falecida',
            'tipo': 'Tipo de Transação',
            'descricao': 'Descrição',
            'valor': 'Valor (R$)',
            'data_vencimento': 'Data de Vencimento',
            'status': 'Status',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personaliza o queryset
        self.fields['pessoa_falecida'].queryset = PessoaFalecida.objects.all()
        self.fields['pessoa_falecida'].empty_label = "Selecione uma pessoa"
        
    def clean_valor(self):
        """Validação personalizada para valor."""
        valor = self.cleaned_data.get('valor')
        if valor is not None and valor <= 0:
            raise forms.ValidationError('O valor deve ser maior que zero.')
        return valor

