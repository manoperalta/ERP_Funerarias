from django import forms
from .models import ServicoContratado
from pessoa_falecida.models import PessoaFalecida
from item_servico.models import ItemServico


class ServicoContratadoForm(forms.ModelForm):
    """Formulário para o modelo ServicoContratado."""
    
    class Meta:
        model = ServicoContratado
        fields = ['pessoa_falecida', 'item_servico', 'descricao_adicional', 'valor_final']
        widgets = {
            'pessoa_falecida': forms.Select(attrs={
                'class': 'form-select'
            }),
            'item_servico': forms.Select(attrs={
                'class': 'form-select'
            }),
            'descricao_adicional': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações adicionais (opcional)'
            }),
            'valor_final': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
        }
        labels = {
            'pessoa_falecida': 'Pessoa Falecida',
            'item_servico': 'Item/Serviço',
            'descricao_adicional': 'Descrição Adicional',
            'valor_final': 'Valor Final (R$)',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personaliza os querysets
        self.fields['pessoa_falecida'].queryset = PessoaFalecida.objects.all()
        self.fields['pessoa_falecida'].empty_label = "Selecione uma pessoa"
        
        self.fields['item_servico'].queryset = ItemServico.objects.all()
        self.fields['item_servico'].empty_label = "Selecione um item/serviço"
        
    def clean_valor_final(self):
        """Validação personalizada para valor final."""
        valor = self.cleaned_data.get('valor_final')
        if valor is not None and valor < 0:
            raise forms.ValidationError('O valor não pode ser negativo.')
        return valor


