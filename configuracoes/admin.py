from django.contrib import admin
from .models import ConfiguracaoFuneraria


@admin.register(ConfiguracaoFuneraria)
class ConfiguracaoFunerariaAdmin(admin.ModelAdmin):
    """Administração das configurações da funerária."""
    
    list_display = [
        'nome_funeraria', 
        'ativa', 
        'telefone_principal', 
        'email_principal',
        'data_atualizacao'
    ]
    
    list_filter = [
        'ativa',
        'data_criacao',
        'data_atualizacao'
    ]
    
    search_fields = [
        'nome_funeraria',
        'cnpj',
        'email_principal',
        'telefone_principal'
    ]
    
    readonly_fields = [
        'data_criacao',
        'data_atualizacao'
    ]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': (
                'nome_funeraria',
                'slogan',
                'ativa'
            )
        }),
        ('Imagens', {
            'fields': (
                'logo',
                'favicon'
            )
        }),
        ('Contato', {
            'fields': (
                'telefone_principal',
                'telefone_secundario',
                'email_principal',
                'email_comercial'
            )
        }),
        ('Endereço', {
            'fields': (
                'endereco_completo',
                'cidade',
                'estado',
                'cep'
            )
        }),
        ('Informações Legais', {
            'fields': (
                'cnpj',
                'inscricao_estadual'
            )
        }),
        ('Redes Sociais', {
            'fields': (
                'facebook_url',
                'instagram_url',
                'whatsapp_numero'
            )
        }),
        ('Aparência', {
            'fields': (
                'cor_primaria',
                'cor_secundaria'
            )
        }),
        ('Funcionamento', {
            'fields': (
                'horario_funcionamento',
            )
        }),
        ('Sistema', {
            'fields': (
                'data_criacao',
                'data_atualizacao'
            ),
            'classes': ('collapse',)
        })
    )
    
    def has_delete_permission(self, request, obj=None):
        """Impede a exclusão se for a única configuração ativa."""
        if obj and obj.ativa:
            # Verifica se é a única configuração ativa
            ativas = ConfiguracaoFuneraria.objects.filter(ativa=True).count()
            if ativas <= 1:
                return False
        return super().has_delete_permission(request, obj)
    
    def save_model(self, request, obj, form, change):
        """Personaliza o salvamento do modelo."""
        super().save_model(request, obj, form, change)
        
        # Mensagem de sucesso personalizada
        if obj.ativa:
            self.message_user(
                request,
                f"Configuração '{obj.nome_funeraria}' ativada com sucesso!"
            )
