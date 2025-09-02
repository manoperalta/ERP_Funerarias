from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Planejamento
from app.mixins import LoginRequiredMixin, AdminDeleteMixin


class PlanejamentoListView(LoginRequiredMixin, ListView):
    """View para listar planejamentos."""
    model = Planejamento
    template_name = 'planejamento/planejamento_list.html'
    context_object_name = 'planejamentos'
    paginate_by = 10


class PlanejamentoDetailView(LoginRequiredMixin, DetailView):
    """View para exibir detalhes de um planejamento."""
    model = Planejamento
    template_name = 'planejamento/planejamento_detail.html'
    context_object_name = 'planejamento'


class PlanejamentoCreateView(LoginRequiredMixin, CreateView):
    """View para criar um novo planejamento."""
    model = Planejamento
    template_name = 'planejamento/planejamento_form.html'
    fields = ['pessoa_falecida', 'nome_plano', 'descricao', 'valor_total']
    success_url = reverse_lazy('planejamento:list')


class PlanejamentoUpdateView(LoginRequiredMixin, UpdateView):
    """View para atualizar um planejamento."""
    model = Planejamento
    template_name = 'planejamento/planejamento_form.html'
    fields = ['pessoa_falecida', 'nome_plano', 'descricao', 'valor_total']
    success_url = reverse_lazy('planejamento:list')


class PlanejamentoDeleteView(AdminDeleteMixin, DeleteView):
    """View para excluir um planejamento. Restrito a administradores."""
    model = Planejamento
    template_name = 'planejamento/planejamento_confirm_delete.html'
    success_url = reverse_lazy('planejamento:list')
