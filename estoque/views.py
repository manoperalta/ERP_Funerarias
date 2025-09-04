from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Sum, F
from datetime import datetime, timedelta

from .models import CategoriaEstoque, ProdutoEstoque, MovimentacaoEstoque, AlertaEstoque
from .forms import CategoriaEstoqueForm, ProdutoEstoqueForm, MovimentacaoEstoqueForm


# Views para CategoriaEstoque
class CategoriaEstoqueListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CategoriaEstoque
    template_name = 'estoque/categoria_list.html'
    context_object_name = 'categorias'
    permission_required = 'estoque.view_categoriaestoque'

class CategoriaEstoqueCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = CategoriaEstoque
    form_class = CategoriaEstoqueForm
    template_name = 'estoque/categoria_form.html'
    success_url = reverse_lazy('estoque:categoria_list')
    permission_required = 'estoque.add_categoriaestoque'

class CategoriaEstoqueUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = CategoriaEstoque
    form_class = CategoriaEstoqueForm
    template_name = 'estoque/categoria_form.html'
    success_url = reverse_lazy('estoque:categoria_list')
    permission_required = 'estoque.change_categoriaestoque'

class CategoriaEstoqueDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = CategoriaEstoque
    template_name = 'estoque/categoria_confirm_delete.html'
    success_url = reverse_lazy('estoque:categoria_list')
    permission_required = 'estoque.delete_categoriaestoque'


# Views para ProdutoEstoque
class ProdutoEstoqueListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ProdutoEstoque
    template_name = 'estoque/produto_list.html'
    context_object_name = 'produtos'
    permission_required = 'estoque.view_produtoestoque'

class ProdutoEstoqueCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ProdutoEstoque
    form_class = ProdutoEstoqueForm
    template_name = 'estoque/produto_form.html'
    success_url = reverse_lazy('estoque:produto_list')
    permission_required = 'estoque.add_produtoestoque'

class ProdutoEstoqueUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ProdutoEstoque
    form_class = ProdutoEstoqueForm
    template_name = 'estoque/produto_form.html'
    success_url = reverse_lazy('estoque:produto_list')
    permission_required = 'estoque.change_produtoestoque'

class ProdutoEstoqueDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ProdutoEstoque
    template_name = 'estoque/produto_confirm_delete.html'
    success_url = reverse_lazy('estoque:produto_list')
    permission_required = 'estoque.delete_produtoestoque'


# Views para MovimentacaoEstoque
class MovimentacaoEstoqueListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = MovimentacaoEstoque
    template_name = 'estoque/movimentacao_list.html'
    context_object_name = 'movimentacoes'
    permission_required = 'estoque.view_movimentacaoestoque'

class MovimentacaoEstoqueCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = MovimentacaoEstoque
    form_class = MovimentacaoEstoqueForm
    template_name = 'estoque/movimentacao_form.html'
    success_url = reverse_lazy('estoque:movimentacao_list')
    permission_required = 'estoque.add_movimentacaoestoque'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class MovimentacaoEstoqueUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = MovimentacaoEstoque
    form_class = MovimentacaoEstoqueForm
    template_name = 'estoque/movimentacao_form.html'
    success_url = reverse_lazy('estoque:movimentacao_list')
    permission_required = 'estoque.change_movimentacaoestoque'

class MovimentacaoEstoqueDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MovimentacaoEstoque
    template_name = 'estoque/movimentacao_confirm_delete.html'
    success_url = reverse_lazy('estoque:movimentacao_list')
    permission_required = 'estoque.delete_movimentacaoestoque'


# View para Relatórios de Estoque
class RelatorioEstoqueView(LoginRequiredMixin, View):
    template_name = 'estoque/relatorios.html'

    def get(self, request, *args, **kwargs):
        # Verificar se o usuário tem permissão de administrador ou acesso ao estoque
        if not (request.user.is_superuser or request.user.cargo == 'administrador'):
            from django.contrib import messages
            messages.error(request, 'Você não tem permissão para acessar os relatórios de estoque.')
            return redirect('accounts:dashboard')
        
        periodo = request.GET.get('periodo', 'diario')
        data_inicio = None
        data_fim = datetime.now()

        if periodo == 'diario':
            data_inicio = data_fim.replace(hour=0, minute=0, second=0, microsecond=0)
        elif periodo == 'semanal':
            data_inicio = data_fim - timedelta(days=data_fim.weekday())
            data_inicio = data_inicio.replace(hour=0, minute=0, second=0, microsecond=0)
        elif periodo == 'mensal':
            data_inicio = data_fim.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif periodo == 'anual':
            data_inicio = data_fim.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

        movimentacoes = MovimentacaoEstoque.objects.filter(
            data_movimentacao__gte=data_inicio,
            data_movimentacao__lte=data_fim
        ).select_related("produto")

        total_entradas = movimentacoes.filter(tipo="entrada").aggregate(total=Sum("quantidade"))["total"] or 0
        total_saidas = movimentacoes.filter(tipo="saida").aggregate(total=Sum("quantidade"))["total"] or 0
        valor_entradas = movimentacoes.filter(tipo="entrada").aggregate(total=Sum(F("quantidade") * F("preco_unitario")))["total"] or 0
        valor_saidas = movimentacoes.filter(tipo="saida").aggregate(total=Sum(F("quantidade") * F("preco_unitario")))["total"] or 0

        context = {
            'periodo': periodo,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'movimentacoes': movimentacoes,
            'total_entradas': total_entradas,
            'total_saidas': total_saidas,
            'valor_entradas': valor_entradas,
            'valor_saidas': valor_saidas,
            'produtos_baixo_estoque': ProdutoEstoque.objects.filter(quantidade_atual__lte=F('quantidade_minima'), ativo=True),
            'alertas_estoque': AlertaEstoque.objects.filter(ativo=True).order_by('-data_criacao')[:10]
        }
        return render(request, self.template_name, context)


# View para Dashboard de Estoque (resumo)
class EstoqueDashboardView(LoginRequiredMixin, View):
    template_name = 'estoque/dashboard.html'

    def get(self, request, *args, **kwargs):
        # Verificar se o usuário tem permissão de administrador ou acesso ao estoque
        if not (request.user.is_superuser or request.user.cargo == 'administrador'):
            from django.contrib import messages
            messages.error(request, 'Você não tem permissão para acessar o controle de estoque.')
            return redirect('accounts:dashboard')
        
        total_produtos = ProdutoEstoque.objects.filter(ativo=True).count()
        produtos_baixo_estoque = ProdutoEstoque.objects.filter(quantidade_atual__lte=F('quantidade_minima'), ativo=True).count()
        total_movimentacoes = MovimentacaoEstoque.objects.count()
        
        # Dados para gráficos (exemplo: últimas 7 movimentações)
        ultimas_movimentacoes = MovimentacaoEstoque.objects.order_by('-data_movimentacao')[:7]

        context = {
            'total_produtos': total_produtos,
            'produtos_baixo_estoque': produtos_baixo_estoque,
            'total_movimentacoes': total_movimentacoes,
            'ultimas_movimentacoes': ultimas_movimentacoes,
            'alertas_recentes': AlertaEstoque.objects.filter(ativo=True).order_by('-data_criacao')[:5]
        }
        return render(request, self.template_name, context)


