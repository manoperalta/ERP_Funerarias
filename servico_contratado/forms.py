from django import forms
from django.forms import inlineformset_factory
from .models import ServicoContratado, ItemServicoContratado
from pessoa_falecida.models import PessoaFalecida
from item_servico.models import ItemServico


class ServicoContratadoForm(forms.ModelForm):
    """Formulário para o modelo ServicoContratado."""
    
    class Meta:
        model = ServicoContratado
        fields = ['pessoa_falecida', 'descricao_adicional', 'taxa_imposto']
        widgets = {
            'pessoa_falecida': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_pessoa_falecida'
            }),
            'descricao_adicional': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações adicionais (opcional)'
            }),
            'taxa_imposto': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '10.00',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'id': 'id_taxa_imposto'
            }),
        }
        labels = {
            'pessoa_falecida': 'Nome do Falecido',
            'descricao_adicional': 'Descrição Adicional',
            'taxa_imposto': 'Taxa de Imposto (%)',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personaliza os querysets
        self.fields['pessoa_falecida'].queryset = PessoaFalecida.objects.all()
        self.fields['pessoa_falecida'].empty_label = "Selecione uma pessoa"
        
    def clean_taxa_imposto(self):
        """Validação personalizada para taxa de imposto."""
        taxa = self.cleaned_data.get('taxa_imposto')
        if taxa is not None and (taxa < 0 or taxa > 100):
            raise forms.ValidationError('A taxa de imposto deve estar entre 0% e 100%.')
        return taxa


class ItemServicoContratadoForm(forms.ModelForm):
    """Formulário para itens individuais do serviço contratado."""
    
    class Meta:
        model = ItemServicoContratado
        fields = ['item_servico', 'quantidade', 'valor_unitario']
        widgets = {
            'item_servico': forms.Select(attrs={
                'class': 'form-select item-servico-select',
                'onchange': 'updateValorUnitario(this)'
            }),
            'quantidade': forms.NumberInput(attrs={
                'class': 'form-control quantidade-input',
                'min': '1',
                'value': '1',
                'onchange': 'calculateTotal(this)'
            }),
            'valor_unitario': forms.NumberInput(attrs={
                'class': 'form-control valor-unitario-input',
                'step': '0.01',
                'min': '0',
                'readonly': 'readonly'
            }),
        }
        labels = {
            'item_servico': 'Item/Serviço',
            'quantidade': 'Quantidade',
            'valor_unitario': 'Valor Unitário (R$)',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item_servico'].queryset = ItemServico.objects.all()
        self.fields['item_servico'].empty_label = "Selecione um item/serviço"


# Formset para múltiplos itens
ItemServicoContratadoFormSet = inlineformset_factory(
    ServicoContratado,
    ItemServicoContratado,
    form=ItemServicoContratadoForm,
    extra=1,
    min_num=1,
    validate_min=True,
    can_delete=True
)

