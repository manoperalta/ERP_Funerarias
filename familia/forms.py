from django import forms
from .models import Familia


class FamiliaForm(forms.ModelForm):
    """Formulário para o modelo Familia."""
    
    class Meta:
        model = Familia
        fields = ['nome_responsavel', 'grau_parentesco', 'telefone', 'email', 'endereco']
        widgets = {
            'nome_responsavel': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do responsável'
            }),
            'grau_parentesco': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Filho, Cônjuge, Pai, Mãe'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemplo.com (opcional)'
            }),
            'endereco': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Digite o endereço completo'
            }),
        }
        labels = {
            'nome_responsavel': 'Nome do Responsável',
            'grau_parentesco': 'Grau de Parentesco',
            'telefone': 'Telefone',
            'email': 'E-mail (Opcional)',
            'endereco': 'Endereço',
        }
        
    def clean_telefone(self):
        """Validação personalizada para telefone."""
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            # Remove caracteres não numéricos para validação
            telefone_numerico = ''.join(filter(str.isdigit, telefone))
            if len(telefone_numerico) < 10:
                raise forms.ValidationError('Telefone deve ter pelo menos 10 dígitos.')
        return telefone

