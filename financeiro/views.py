from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Financeiro


class FinanceiroListView(ListView):
    """View para listar registros financeiros."""
    model = Financeiro
    template_name = 'financeiro/financeiro_list.html'
    context_object_name = 'financeiros'
    paginate_by = 10


class FinanceiroDetailView(DetailView):
    """View para exibir detalhes de um registro financeiro."""
    model = Financeiro
    template_name = 'financeiro/financeiro_detail.html'
    context_object_name = 'financeiro'


class FinanceiroCreateView(CreateView):
    """View para criar um novo registro financeiro."""
    model = Financeiro
    template_name = 'financeiro/financeiro_form.html'
    fields = ['pessoa_falecida', 'tipo', 'descricao', 'valor', 'data_vencimento', 'status']
    success_url = reverse_lazy('financeiro:list')


class FinanceiroUpdateView(UpdateView):
    """View para atualizar um registro financeiro."""
    model = Financeiro
    template_name = 'financeiro/financeiro_form.html'
    fields = ['pessoa_falecida', 'tipo', 'descricao', 'valor', 'data_vencimento', 'status']
    success_url = reverse_lazy('financeiro:list')


class FinanceiroDeleteView(DeleteView):
    """View para excluir um registro financeiro."""
    model = Financeiro
    template_name = 'financeiro/financeiro_confirm_delete.html'
    success_url = reverse_lazy('financeiro:list')
