from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import PessoaFalecida
from .forms import PessoaFalecidaForm
from app.mixins import LoginRequiredMixin, AdminDeleteMixin


class PessoaFalecidaListView(LoginRequiredMixin, ListView):
    """View para listar pessoas falecidas."""
    model = PessoaFalecida
    template_name = 'pessoa_falecida/pessoa_falecida_list.html'
    context_object_name = 'pessoas_falecidas'
    paginate_by = 10


class PessoaFalecidaDetailView(LoginRequiredMixin, DetailView):
    """View para exibir detalhes de uma pessoa falecida."""
    model = PessoaFalecida
    template_name = 'pessoa_falecida/pessoa_falecida_detail.html'
    context_object_name = 'pessoa_falecida'


class PessoaFalecidaCreateView(LoginRequiredMixin, CreateView):
    """View para criar uma nova pessoa falecida."""
    model = PessoaFalecida
    form_class = PessoaFalecidaForm
    template_name = 'pessoa_falecida/pessoa_falecida_form.html'
    success_url = reverse_lazy('pessoa_falecida:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nova Pessoa Falecida'
        return context


class PessoaFalecidaUpdateView(LoginRequiredMixin, UpdateView):
    """View para atualizar uma pessoa falecida."""
    model = PessoaFalecida
    form_class = PessoaFalecidaForm
    template_name = 'pessoa_falecida/pessoa_falecida_form.html'
    success_url = reverse_lazy('pessoa_falecida:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Pessoa Falecida'
        return context


class PessoaFalecidaDeleteView(AdminDeleteMixin, DeleteView):
    """View para excluir uma pessoa falecida. Restrito a administradores."""
    model = PessoaFalecida
    template_name = 'pessoa_falecida/pessoa_falecida_confirm_delete.html'
    success_url = reverse_lazy('pessoa_falecida:list')
