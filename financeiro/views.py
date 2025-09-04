from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Sum, Count, Q
from .models import Financeiro
from app.mixins import LoginRequiredMixin, AdminDeleteMixin


class FinanceiroListView(LoginRequiredMixin, ListView):
    """View para listar registros financeiros."""
    model = Financeiro
    template_name = 'financeiro/financeiro_list.html'
    context_object_name = 'financeiros'
    paginate_by = 10
    
    def get_queryset(self):
        """Filtrar por status se especificado."""
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Financeiro.STATUS_CHOICES
        context['status_atual'] = self.request.GET.get('status', '')
        
        # Calcular valores para os cards
        context.update(self.get_financial_summary())
        
        return context
    
    def get_financial_summary(self):
        """Calcula o resumo financeiro para os cards."""
        # Receitas pagas
        receitas_pagas = Financeiro.objects.filter(
            tipo='receita',
            status='pago'
        ).aggregate(total=Sum('valor'))['total'] or 0
        
        # Pendentes (receitas e despesas)
        pendentes_count = Financeiro.objects.filter(
            status='pendente'
        ).count()
        
        # Despesas (total de despesas pagas)
        despesas_total = Financeiro.objects.filter(
            tipo='despesa',
            status='pago'
        ).aggregate(total=Sum('valor'))['total'] or 0
        
        # Com nota fiscal (registros que têm nota fiscal)
        com_nota_fiscal_count = Financeiro.objects.filter(
            servico_contratado__isnull=False,
            servico_contratado__pdf_nota_fiscal__isnull=False
        ).exclude(
            servico_contratado__pdf_nota_fiscal=''
        ).count()
        
        return {
            'receitas_pagas': receitas_pagas,
            'pendentes_count': pendentes_count,
            'despesas_total': despesas_total,
            'com_nota_fiscal_count': com_nota_fiscal_count,
        }


class FinanceiroDetailView(LoginRequiredMixin, DetailView):
    """View para exibir detalhes de um registro financeiro."""
    model = Financeiro
    template_name = 'financeiro/financeiro_detail.html'
    context_object_name = 'financeiro'


class FinanceiroCreateView(LoginRequiredMixin, CreateView):
    """View para criar um novo registro financeiro."""
    model = Financeiro
    template_name = 'financeiro/financeiro_form.html'
    fields = [
        'pessoa_falecida', 'servico_contratado', 'tipo', 'descricao', 
        'valor', 'data_vencimento', 'forma_pagamento', 'status', 'observacoes'
    ]
    success_url = reverse_lazy('financeiro:list')


class FinanceiroUpdateView(LoginRequiredMixin, UpdateView):
    """View para atualizar um registro financeiro."""
    model = Financeiro
    template_name = 'financeiro/financeiro_form.html'
    fields = [
        'pessoa_falecida', 'servico_contratado', 'tipo', 'descricao', 
        'valor', 'data_vencimento', 'forma_pagamento', 'status', 'observacoes'
    ]
    success_url = reverse_lazy('financeiro:list')


class FinanceiroDeleteView(AdminDeleteMixin, DeleteView):
    """View para excluir um registro financeiro. Restrito a administradores."""
    model = Financeiro
    template_name = 'financeiro/financeiro_confirm_delete.html'
    success_url = reverse_lazy('financeiro:list')


@login_required
def marcar_como_pago(request, pk):
    """Marca um registro financeiro como pago."""
    financeiro = get_object_or_404(Financeiro, pk=pk)
    forma_pagamento = request.POST.get('forma_pagamento')
    
    financeiro.marcar_como_pago(forma_pagamento)
    messages.success(request, f'Registro financeiro marcado como pago.')
    
    return redirect('financeiro:detail', pk=pk)


@login_required
def visualizar_nota_fiscal(request, pk):
    """Visualiza a nota fiscal associada ao registro financeiro."""
    financeiro = get_object_or_404(Financeiro, pk=pk)
    
    if not financeiro.servico_contratado or not financeiro.servico_contratado.pdf_nota_fiscal:
        messages.error(request, 'Nota fiscal não encontrada para este registro.')
        return redirect('financeiro:detail', pk=pk)
    
    # Redirecionar para a view de visualização do PDF do serviço contratado
    return redirect('servico_contratado:visualizar_pdf', pk=financeiro.servico_contratado.pk)
