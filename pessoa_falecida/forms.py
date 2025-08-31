from django import forms
from .models import PessoaFalecida
from familia.models import Familia


class PessoaFalecidaForm(forms.ModelForm):
    """Formulário para o modelo PessoaFalecida."""
    
    class Meta:
        model = PessoaFalecida
        fields = ['nome', 'data_nascimento', 'data_falecimento', 'causa_obito', 'local_obito', 'documento_cpf_rg', 'familia', 'imagem']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome completo'
            }),
            'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'data_falecimento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'causa_obito': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descreva a causa do óbito'
            }),
            'local_obito': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Local onde ocorreu o óbito'
            }),
            'documento_cpf_rg': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'CPF ou RG'
            }),
            'familia': forms.Select(attrs={
                'class': 'form-select'
            }),
            'imagem': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'nome': 'Nome Completo',
            'data_nascimento': 'Data de Nascimento',
            'data_falecimento': 'Data de Falecimento',
            'causa_obito': 'Causa do Óbito',
            'local_obito': 'Local do Óbito',
            'documento_cpf_rg': 'Documento (CPF/RG)',
            'familia': 'Família Responsável',
            'imagem': 'Foto do Falecido',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personaliza o queryset da família para mostrar nome do responsável
        self.fields['familia'].queryset = Familia.objects.all()
        self.fields['familia'].empty_label = "Selecione uma família"
        
    def clean(self):
        """Validação personalizada para datas."""
        cleaned_data = super().clean()
        data_nascimento = cleaned_data.get('data_nascimento')
        data_falecimento = cleaned_data.get('data_falecimento')
        
        if data_nascimento and data_falecimento:
            if data_nascimento >= data_falecimento:
                raise forms.ValidationError(
                    'A data de nascimento deve ser anterior à data de falecimento.'
                )
                
        return cleaned_data
        
    def clean_documento_cpf_rg(self):
        """Validação personalizada para documento."""
        documento = self.cleaned_data.get('documento_cpf_rg')
        if documento:
            # Remove caracteres não numéricos
            documento_numerico = ''.join(filter(str.isdigit, documento))
            if len(documento_numerico) not in [11, 9]:  # CPF tem 11 dígitos, RG pode ter 9
                raise forms.ValidationError('Documento deve ter 9 (RG) ou 11 (CPF) dígitos.')
        return documento

