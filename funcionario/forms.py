from django import forms
from .models import Funcionario


class FuncionarioForm(forms.ModelForm):
    """Formulário para o modelo Funcionario."""
    
    class Meta:
        model = Funcionario
        fields = ['nome', 'cargo', 'telefone', 'email']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome completo'
            }),
            'cargo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o cargo'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemplo.com'
            }),
        }
        labels = {
            'nome': 'Nome Completo',
            'cargo': 'Cargo',
            'telefone': 'Telefone',
            'email': 'E-mail',
        }
        
    def clean_email(self):
        """Validação personalizada para email."""
        email = self.cleaned_data.get('email')
        if email:
            # Verifica se já existe outro funcionário com o mesmo email
            existing = Funcionario.objects.filter(email=email)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise forms.ValidationError('Já existe um funcionário com este email.')
        return email
        
    def clean_telefone(self):
        """Validação personalizada para telefone."""
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            # Remove caracteres não numéricos para validação
            telefone_numerico = ''.join(filter(str.isdigit, telefone))
            if len(telefone_numerico) < 10:
                raise forms.ValidationError('Telefone deve ter pelo menos 10 dígitos.')
        return telefone

