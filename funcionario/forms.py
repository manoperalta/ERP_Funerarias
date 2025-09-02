from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Funcionario
from accounts.models import CustomUser


class FuncionarioForm(forms.ModelForm):
    """Formulário para o modelo Funcionario (apenas edição)."""
    
    class Meta:
        model = Funcionario
        fields = ['nome', 'cargo', 'telefone', 'email', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome completo'
            }),
            'cargo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemplo.com'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'nome': 'Nome Completo',
            'cargo': 'Cargo',
            'telefone': 'Telefone',
            'email': 'E-mail',
            'ativo': 'Funcionário Ativo',
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


class FuncionarioUsuarioForm(UserCreationForm):
    """Formulário integrado para criar funcionário + usuário (similar ao register)."""
    
    # Campos do funcionário
    nome_completo = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome completo do funcionário'
        }),
        label='Nome Completo'
    )
    telefone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(11) 99999-9999'
        }),
        label='Telefone'
    )
    
    # Campos do usuário (herdados e customizados)
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'cargo', 
                 'telefone', 'foto_perfil', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome de usuário para login'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemplo.com'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Primeiro nome'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sobrenome'
            }),
            'cargo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'foto_perfil': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'username': 'Nome de Usuário',
            'email': 'E-mail',
            'first_name': 'Primeiro Nome',
            'last_name': 'Sobrenome',
            'cargo': 'Cargo',
            'foto_perfil': 'Foto do Perfil',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Personaliza os campos de senha
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Digite a senha'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirme a senha'
        })
        self.fields['password1'].label = 'Senha'
        self.fields['password2'].label = 'Confirmar Senha'
        
        # Torna campos obrigatórios
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['cargo'].required = True
        self.fields['nome_completo'].required = True
        self.fields['telefone'].required = True
        
        # Remove opção de administrador para funcionários
        cargo_choices = [choice for choice in CustomUser.CARGO_CHOICES if choice[0] != 'adm']
        self.fields['cargo'].choices = cargo_choices
        
        # Define ordem dos campos
        self.field_order = [
            'nome_completo', 'first_name', 'last_name', 'email', 'telefone',
            'cargo', 'username', 'password1', 'password2', 'foto_perfil'
        ]
    
    def clean_nome_completo(self):
        """Validação do nome completo."""
        nome = self.cleaned_data.get('nome_completo')
        if nome and len(nome.split()) < 2:
            raise forms.ValidationError('Digite o nome completo (nome e sobrenome).')
        return nome
    
    def clean_email(self):
        """Validação de email único."""
        email = self.cleaned_data.get('email')
        if email:
            # Verifica se já existe funcionário com este email
            if Funcionario.objects.filter(email=email).exists():
                raise forms.ValidationError('Já existe um funcionário com este email.')
            # Verifica se já existe usuário com este email
            if CustomUser.objects.filter(email=email).exists():
                raise forms.ValidationError('Já existe um usuário com este email.')
        return email
    
    def clean_telefone(self):
        """Validação de telefone."""
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            telefone_numerico = ''.join(filter(str.isdigit, telefone))
            if len(telefone_numerico) < 10:
                raise forms.ValidationError('Telefone deve ter pelo menos 10 dígitos.')
        return telefone
    
    def clean(self):
        """Validação geral do formulário."""
        cleaned_data = super().clean()
        
        # Sincronizar nome completo com first_name e last_name
        nome_completo = cleaned_data.get('nome_completo')
        if nome_completo:
            nome_parts = nome_completo.split()
            if len(nome_parts) >= 2:
                cleaned_data['first_name'] = nome_parts[0]
                cleaned_data['last_name'] = ' '.join(nome_parts[1:])
        
        return cleaned_data
    
    def save(self, commit=True):
        """Salva usuário e cria funcionário associado."""
        # Salva o usuário
        usuario = super().save(commit=commit)
        
        if commit:
            # Cria o funcionário associado
            funcionario = Funcionario.objects.create(
                nome=self.cleaned_data['nome_completo'],
                cargo=usuario.cargo,
                telefone=self.cleaned_data['telefone'],
                email=usuario.email,
                usuario=usuario,
                ativo=True
            )
            
            return funcionario
        
        return usuario

