from django import forms
from .models import ConfiguracaoFuneraria


class ConfiguracaoFunerariaForm(forms.ModelForm):
    """Formulário para configurações da funerária."""
    
    class Meta:
        model = ConfiguracaoFuneraria
        fields = [
            'nome_funeraria', 'slogan', 'logo', 'favicon',
            'telefone_principal', 'telefone_secundario',
            'email_principal', 'email_comercial',
            'endereco_completo', 'cep', 'cidade', 'estado',
            'cnpj', 'inscricao_estadual',
            'facebook_url', 'instagram_url', 'whatsapp_numero',
            'cor_primaria', 'cor_secundaria',
            'horario_funcionamento'
        ]
        
        widgets = {
            'nome_funeraria': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da funerária'
            }),
            'slogan': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Slogan da funerária'
            }),
            'logo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'favicon': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'telefone_principal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999'
            }),
            'telefone_secundario': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999'
            }),
            'email_principal': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'contato@funeraria.com'
            }),
            'email_comercial': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'comercial@funeraria.com'
            }),
            'endereco_completo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Endereço completo da funerária'
            }),
            'cep': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '12345-678'
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'São Paulo'
            }),
            'estado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SP',
                'maxlength': '2'
            }),
            'cnpj': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '12.345.678/0001-90'
            }),
            'inscricao_estadual': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Inscrição Estadual'
            }),
            'facebook_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://facebook.com/funeraria'
            }),
            'instagram_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://instagram.com/funeraria'
            }),
            'whatsapp_numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '5511999999999'
            }),
            'cor_primaria': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color'
            }),
            'cor_secundaria': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color'
            }),
            'horario_funcionamento': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Segunda a Sexta: 8h às 18h\nSábado: 8h às 12h\nDomingo: Plantão 24h'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Adiciona classes CSS e configurações extras
        for field_name, field in self.fields.items():
            if field.required:
                field.widget.attrs['required'] = True
            
            # Adiciona help_text como placeholder se não houver placeholder
            if hasattr(field, 'help_text') and field.help_text:
                if 'placeholder' not in field.widget.attrs:
                    field.widget.attrs['placeholder'] = field.help_text
    
    def clean_estado(self):
        """Valida o campo estado."""
        estado = self.cleaned_data.get('estado')
        if estado:
            return estado.upper()
        return estado
    
    def clean_whatsapp_numero(self):
        """Valida o número do WhatsApp."""
        numero = self.cleaned_data.get('whatsapp_numero')
        if numero:
            # Remove caracteres não numéricos
            numero_limpo = ''.join(filter(str.isdigit, numero))
            if len(numero_limpo) < 10:
                raise forms.ValidationError(
                    'Número do WhatsApp deve ter pelo menos 10 dígitos.'
                )
            return numero_limpo
        return numero

