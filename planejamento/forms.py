from django import forms
from .models import Planejamento
from pessoa_falecida.models import PessoaFalecida


class PlanejamentoForm(forms.ModelForm):
    """Formulário para o modelo Planejamento."""
    
    class Meta:
        model = Planejamento
        fields = ['nome_plano', 'pessoa_falecida', 'descricao', 'valor_total']
        widgets = {
            'nome_plano': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do plano'
            }),
            'pessoa_falecida': forms.Select(attrs={
                'class': 'form-select'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descrição detalhada do planejamento'
            }),
            'valor_total': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
        }
        labels = {
            'nome_plano': 'Nome do Plano',
            'pessoa_falecida': 'Pessoa Falecida',
            'descricao': 'Descrição do Planejamento',
            'valor_total': 'Valor Total (R$)',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personaliza o queryset
        self.fields['pessoa_falecida'].queryset = PessoaFalecida.objects.all()
        self.fields['pessoa_falecida'].empty_label = "Selecione uma pessoa"
        
    def clean_valor_total(self):
        """Validação personalizada para valor total."""
        valor = self.cleaned_data.get('valor_total')
        if valor is not None and valor < 0:
            raise forms.ValidationError('O valor não pode ser negativo.')
        return valor

