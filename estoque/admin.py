from django.contrib import admin
from .models import CategoriaEstoque, ProdutoEstoque, MovimentacaoEstoque, AlertaEstoque

@admin.register(CategoriaEstoque)
class CategoriaEstoqueAdmin(admin.ModelAdmin):
    list_display = (
        'nome', 'ativa', 'data_criacao'
    )
    search_fields = ('nome',)
    list_filter = ('ativa',)

@admin.register(ProdutoEstoque)
class ProdutoEstoqueAdmin(admin.ModelAdmin):
    list_display = (
        'codigo', 'nome', 'categoria', 'quantidade_atual', 'quantidade_minima', 
        'preco_custo', 'preco_venda', 'ativo', 'data_atualizacao'
    )
    search_fields = ('codigo', 'nome', 'descricao')
    list_filter = ('categoria', 'ativo', 'unidade_medida')
    list_editable = ('quantidade_atual', 'preco_custo', 'preco_venda', 'ativo')
    raw_id_fields = ('categoria',)
    fieldsets = (
        (None, {
            'fields': (
                ('codigo', 'nome'),
                'descricao',
                ('categoria', 'unidade_medida'),
                ('preco_custo', 'preco_venda'),
                ('quantidade_atual', 'quantidade_minima', 'quantidade_maxima'),
                'localizacao',
                'ativo',
            )
        }),
    )

@admin.register(MovimentacaoEstoque)
class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    list_display = (
        'produto', 'tipo', 'quantidade', 'preco_unitario', 'valor_total', 
        'usuario', 'data_movimentacao'
    )
    search_fields = ('produto__nome', 'observacoes', 'documento', 'fornecedor')
    list_filter = ('tipo', 'data_movimentacao', 'usuario')
    raw_id_fields = ('produto', 'usuario')
    readonly_fields = ('data_movimentacao', 'valor_total')

@admin.register(AlertaEstoque)
class AlertaEstoqueAdmin(admin.ModelAdmin):
    list_display = (
        'produto', 'tipo_alerta', 'mensagem', 'ativo', 'data_criacao', 'data_resolucao'
    )
    search_fields = ('produto__nome', 'mensagem')
    list_filter = ('tipo_alerta', 'ativo', 'data_criacao')
    raw_id_fields = ('produto',)
    readonly_fields = ('data_criacao',)


