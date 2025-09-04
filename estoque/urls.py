from django.urls import path
from . import views

app_name = 'estoque'

urlpatterns = [
    # URLs para CategoriaEstoque
    path("categorias/", views.CategoriaEstoqueListView.as_view(), name="categoria_list"),
    path("categorias/nova/", views.CategoriaEstoqueCreateView.as_view(), name="categoria_create"),
    path("categorias/<int:pk>/editar/", views.CategoriaEstoqueUpdateView.as_view(), name="categoria_update"),
    path("categorias/<int:pk>/excluir/", views.CategoriaEstoqueDeleteView.as_view(), name="categoria_delete"),

    # URLs para ProdutoEstoque
    path("produtos/", views.ProdutoEstoqueListView.as_view(), name="produto_list"),
    path("produtos/novo/", views.ProdutoEstoqueCreateView.as_view(), name="produto_create"),
    path("produtos/<int:pk>/editar/", views.ProdutoEstoqueUpdateView.as_view(), name="produto_update"),
    path("produtos/<int:pk>/excluir/", views.ProdutoEstoqueDeleteView.as_view(), name="produto_delete"),

    # URLs para MovimentacaoEstoque
    path("movimentacoes/", views.MovimentacaoEstoqueListView.as_view(), name="movimentacao_list"),
    path("movimentacoes/nova/", views.MovimentacaoEstoqueCreateView.as_view(), name="movimentacao_create"),
    path("movimentacoes/<int:pk>/editar/", views.MovimentacaoEstoqueUpdateView.as_view(), name="movimentacao_update"),
    path("movimentacoes/<int:pk>/excluir/", views.MovimentacaoEstoqueDeleteView.as_view(), name="movimentacao_delete"),

    # URLs para Relatórios e Dashboard
    path("relatorios/", views.RelatorioEstoqueView.as_view(), name="relatorios"),
    path("dashboard/", views.EstoqueDashboardView.as_view(), name="dashboard"),
]


