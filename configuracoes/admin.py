from django.contrib import admin
from .models import ConfiguracaoFuneraria


@admin.register(ConfiguracaoFuneraria)
class ConfiguracaoFunerariaAdmin(admin.ModelAdmin):
    list_display = (
        'nome_funeraria', 'telefone_principal', 'email_principal', 
        'cidade', 'estado', 'ativa'
    )
    list_filter = (
        'ativa', 'cidade', 'estado'
    )
    search_fields = (
        'nome_funeraria', 'telefone_principal', 'email_principal', 
        'endereco_completo', 'cnpj'
    )
    fieldsets = (
        (None, {
            'fields': (
                'nome_funeraria', 'slogan', 'logo', 'favicon', 'ativa'
            )
        }),
        ('Informações de Contato', {
            'fields': (
                'telefone_principal', 'telefone_secundario', 
                'email_principal', 'email_comercial'
            )
        }),
        ('Endereço', {
            'fields': (
                'endereco_completo', 'cep', 'cidade', 'estado'
            )
        }),
        ('Informações Legais', {
            'fields': (
                'cnpj', 'inscricao_estadual'
            )
        }),
        ('Redes Sociais', {
            'fields': (
                'facebook_url', 'instagram_url', 'whatsapp_numero'
            )
        }),
        ('Aparência', {
            'fields': (
                'cor_primaria', 'cor_secundaria'
            )
        }),
        ('Outros', {
            'fields': (
                'horario_funcionamento', 'data_criacao', 'data_atualizacao'
            )
        }),
    )
    readonly_fields = ('data_criacao', 'data_atualizacao')

    def has_add_permission(self, request):
        # Permite adicionar apenas se não houver nenhuma configuração ativa
        return not ConfiguracaoFuneraria.objects.filter(ativa=True).exists()

    def has_delete_permission(self, request, obj=None):
        # Permite deletar apenas se não for a configuração ativa
        if obj and obj.ativa:
            return False
        return True