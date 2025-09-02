from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Familia
from .forms import FamiliaForm
from app.mixins import LoginRequiredMixin, AdminDeleteMixin


class FamiliaListView(LoginRequiredMixin, ListView):
    """View para listar famílias."""
    model = Familia
    template_name = 'familia/familia_list.html'
    context_object_name = 'familias'
    paginate_by = 10


class FamiliaDetailView(LoginRequiredMixin, DetailView):
    """View para exibir detalhes de uma família."""
    model = Familia
    template_name = 'familia/familia_detail.html'
    context_object_name = 'familia'


class FamiliaCreateView(LoginRequiredMixin, CreateView):
    """View para criar uma nova família."""
    model = Familia
    form_class = FamiliaForm
    template_name = 'familia/familia_form.html'
    success_url = reverse_lazy('familia:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nova Família'
        return context


class FamiliaUpdateView(LoginRequiredMixin, UpdateView):
    """View para atualizar uma família."""
    model = Familia
    form_class = FamiliaForm
    template_name = 'familia/familia_form.html'
    success_url = reverse_lazy('familia:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Família'
        return context


class FamiliaDeleteView(AdminDeleteMixin, DeleteView):
    """View para excluir uma família. Restrito a administradores."""
    model = Familia
    template_name = 'familia/familia_confirm_delete.html'
    success_url = reverse_lazy('familia:list')
