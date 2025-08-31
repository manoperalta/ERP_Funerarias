from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Funcionario
from .forms import FuncionarioForm


class FuncionarioListView(ListView):
    """View para listar funcionários."""
    model = Funcionario
    template_name = 'funcionario/funcionario_list.html'
    context_object_name = 'funcionarios'
    paginate_by = 10


class FuncionarioDetailView(DetailView):
    """View para exibir detalhes de um funcionário."""
    model = Funcionario
    template_name = 'funcionario/funcionario_detail.html'
    context_object_name = 'funcionario'


class FuncionarioCreateView(CreateView):
    """View para criar um novo funcionário."""
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'funcionario/funcionario_form.html'
    success_url = reverse_lazy('funcionario:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Novo Funcionário'
        return context


class FuncionarioUpdateView(UpdateView):
    """View para atualizar um funcionário."""
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'funcionario/funcionario_form.html'
    success_url = reverse_lazy('funcionario:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Funcionário'
        return context


class FuncionarioDeleteView(DeleteView):
    """View para excluir um funcionário."""
    model = Funcionario
    template_name = 'funcionario/funcionario_confirm_delete.html'
    success_url = reverse_lazy('funcionario:list')
