from django.contrib import admin
from .models import TemplateDocumento, DocumentoGerado, CompartilhamentoDocumento, MetaTagsDocumento


@admin.register(TemplateDocumento)
class TemplateDocumentoAdmin(admin.ModelAdmin):
    list_display = (
        'nome', 'tipo', 'ativo', 'padrao', 'data_criacao', 'data_atualizacao'
    )
    list_filter = (
        'tipo', 'ativo', 'padrao', 'data_criacao'
    )
    search_fields = (
        'nome', 'descricao', 'conteudo_html'
    )
    readonly_fields = (
        'data_criacao', 'data_atualizacao'
    )
    fieldsets = (
        (None, {
            'fields': (
                'nome', 'tipo', 'descricao', 'ativo', 'padrao'
            )
        }),
        ('Conteúdo', {
            'fields': (
                'conteudo_html', 'css_personalizado', 'variaveis_disponiveis'
            )
        }),
        ('Datas', {
            'fields': (
                'data_criacao', 'data_atualizacao'
            )
        }),
    )


@admin.register(DocumentoGerado)
class DocumentoGeradoAdmin(admin.ModelAdmin):
    list_display = (
        'titulo', 'template', 'pessoa_falecida', 'familia', 
        'servico_contratado', 'status', 'publico', 'visualizacoes', 
        'usuario_criador', 'data_criacao'
    )
    list_filter = (
        'template', 'status', 'publico', 'data_criacao', 'usuario_criador'
    )
    search_fields = (
        'titulo', 'conteudo_html', 'pessoa_falecida__nome', 
        'familia__nome_responsavel', 'servico_contratado__item_servico__nome'
    )
    readonly_fields = (
        'uuid', 'arquivo_pdf', 'visualizacoes', 'data_criacao', 'data_atualizacao'
    )
    raw_id_fields = (
        'template', 'pessoa_falecida', 'familia', 'servico_contratado', 'usuario_criador'
    )
    fieldsets = (
        (None, {
            'fields': (
                'uuid', 'titulo', 'template', 'pessoa_falecida', 'familia', 
                'servico_contratado', 'conteudo_html', 'arquivo_pdf', 'status', 
                'publico', 'senha_acesso', 'data_expiracao', 'visualizacoes', 
                'usuario_criador'
            )
        }),
        ('Datas', {
            'fields': (
                'data_criacao', 'data_atualizacao'
            )
        }),
    )


@admin.register(CompartilhamentoDocumento)
class CompartilhamentoDocumentoAdmin(admin.ModelAdmin):
    list_display = (
        'documento', 'plataforma', 'destinatario', 'data_compartilhamento', 'usuario'
    )
    list_filter = (
        'plataforma', 'data_compartilhamento', 'usuario'
    )
    search_fields = (
        'documento__titulo', 'destinatario', 'mensagem_personalizada'
    )
    readonly_fields = (
        'data_compartilhamento',
    )
    raw_id_fields = (
        'documento', 'usuario',
    )


@admin.register(MetaTagsDocumento)
class MetaTagsDocumentoAdmin(admin.ModelAdmin):
    list_display = (
        'documento', 'og_title', 'twitter_title', 'whatsapp_title'
    )
    search_fields = (
        'documento__titulo', 'og_title', 'twitter_title', 'whatsapp_title'
    )
    raw_id_fields = (
        'documento',
    )


