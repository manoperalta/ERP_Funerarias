from django.contrib import admin
from .models import CategoriaEstoque, ProdutoEstoque, MovimentacaoEstoque, AlertaEstoque


@admin.register(CategoriaEstoque)
class CategoriaEstoqueAdmin(admin.ModelAdmin):
    list_display = (
        'nome', 'descricao', 'cor', 'ativa', 'data_criacao'
    )
    list_filter = (
        'ativa', 'data_criacao'
    )
    search_fields = (
        'nome', 'descricao'
    )


@admin.register(ProdutoEstoque)
class ProdutoEstoqueAdmin(admin.ModelAdmin):
    list_display = (
        'codigo', 'nome', 'categoria', 'unidade_medida', 'preco_venda', 
        'quantidade_atual', 'quantidade_minima', 'ativo', 'estoque_baixo'
    )
    list_filter = (
        'categoria', 'unidade_medida', 'ativo', 'quantidade_minima'
    )
    search_fields = (
        'codigo', 'nome', 'descricao'
    )
    readonly_fields = (
        'data_criacao', 'data_atualizacao'
    )
    fieldsets = (
        (None, {
            'fields': (
                'codigo', 'nome', 'descricao', 'categoria', 'unidade_medida', 
                'preco_custo', 'preco_venda', 'quantidade_atual', 
                'quantidade_minima', 'quantidade_maxima', 'localizacao', 'ativo'
            )
        }),
        ('Datas', {
            'fields': (
                'data_criacao', 'data_atualizacao'
            )
        }),
    )


@admin.register(MovimentacaoEstoque)
class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    list_display = (
        'produto', 'tipo', 'quantidade', 'preco_unitario', 'valor_total', 
        'documento', 'fornecedor', 'usuario', 'data_movimentacao'
    )
    list_filter = (
        'tipo', 'data_movimentacao', 'usuario'
    )
    search_fields = (
        'produto__nome', 'documento', 'fornecedor', 'observacoes'
    )
    readonly_fields = (
        'data_movimentacao',
    )
    raw_id_fields = (
        'produto', 'usuario',
    )


@admin.register(AlertaEstoque)
class AlertaEstoqueAdmin(admin.ModelAdmin):
    list_display = (
        'produto', 'tipo_alerta', 'mensagem', 'ativo', 'data_criacao', 'data_resolucao'
    )
    list_filter = (
        'tipo_alerta', 'ativo', 'data_criacao'
    )
    search_fields = (
        'produto__nome', 'mensagem'
    )
    readonly_fields = (
        'data_criacao', 'data_resolucao',
    )
    raw_id_fields = (
        'produto',
    )


