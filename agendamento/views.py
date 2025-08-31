from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Agendamento
from .forms import AgendamentoForm


class AgendamentoListView(ListView):
    """View para listar agendamentos."""
    model = Agendamento
    template_name = 'agendamento/agendamento_list.html'
    context_object_name = 'agendamentos'
    paginate_by = 10


class AgendamentoDetailView(DetailView):
    """View para exibir detalhes de um agendamento."""
    model = Agendamento
    template_name = 'agendamento/agendamento_detail.html'
    context_object_name = 'agendamento'


class AgendamentoCreateView(CreateView):
    """View para criar um novo agendamento."""
    model = Agendamento
    template_name = 'agendamento/agendamento_form.html'
    form_class = AgendamentoForm
    success_url = reverse_lazy('agendamento:list')


class AgendamentoUpdateView(UpdateView):
    """View para atualizar um agendamento."""
    model = Agendamento
    template_name = 'agendamento/agendamento_form.html'
    form_class = AgendamentoForm
    success_url = reverse_lazy('agendamento:list')


class AgendamentoDeleteView(DeleteView):
    """View para excluir um agendamento."""
    model = Agendamento
    template_name = 'agendamento/agendamento_confirm_delete.html'
    success_url = reverse_lazy('agendamento:list')
