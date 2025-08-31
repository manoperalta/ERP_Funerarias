from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import ServicoContratado


class ServicoContratadoListView(ListView):
    """View para listar serviços contratados."""
    model = ServicoContratado
    template_name = 'servico_contratado/servico_contratado_list.html'
    context_object_name = 'servicos_contratados'
    paginate_by = 10


class ServicoContratadoDetailView(DetailView):
    """View para exibir detalhes de um serviço contratado."""
    model = ServicoContratado
    template_name = 'servico_contratado/servico_contratado_detail.html'
    context_object_name = 'servico_contratado'


class ServicoContratadoCreateView(CreateView):
    """View para criar um novo serviço contratado."""
    model = ServicoContratado
    template_name = 'servico_contratado/servico_contratado_form.html'
    fields = ['pessoa_falecida', 'item_servico', 'descricao_adicional', 'valor_final']
    success_url = reverse_lazy('servico_contratado:list')


class ServicoContratadoUpdateView(UpdateView):
    """View para atualizar um serviço contratado."""
    model = ServicoContratado
    template_name = 'servico_contratado/servico_contratado_form.html'
    fields = ['pessoa_falecida', 'item_servico', 'descricao_adicional', 'valor_final']
    success_url = reverse_lazy('servico_contratado:list')


class ServicoContratadoDeleteView(DeleteView):
    """View para excluir um serviço contratado."""
    model = ServicoContratado
    template_name = 'servico_contratado/servico_contratado_confirm_delete.html'
    success_url = reverse_lazy('servico_contratado:list')
