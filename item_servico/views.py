from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import ItemServico
from .forms import ItemServicoForm


class ItemServicoListView(ListView):
    """View para listar itens de serviço."""
    model = ItemServico
    template_name = 'item_servico/item_servico_list.html'
    context_object_name = 'itens_servico'
    paginate_by = 10


class ItemServicoDetailView(DetailView):
    """View para exibir detalhes de um item de serviço."""
    model = ItemServico
    template_name = 'item_servico/item_servico_detail.html'
    context_object_name = 'item_servico'


class ItemServicoCreateView(CreateView):
    """View para criar um novo item de serviço."""
    model = ItemServico
    form_class = ItemServicoForm
    template_name = 'item_servico/item_servico_form.html'
    success_url = reverse_lazy('item_servico:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Novo Item/Serviço'
        return context


class ItemServicoUpdateView(UpdateView):
    """View para atualizar um item de serviço."""
    model = ItemServico
    form_class = ItemServicoForm
    template_name = 'item_servico/item_servico_form.html'
    success_url = reverse_lazy('item_servico:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Item/Serviço'
        return context


class ItemServicoDeleteView(DeleteView):
    """View para excluir um item de serviço."""
    model = ItemServico
    template_name = 'item_servico/item_servico_confirm_delete.html'
    success_url = reverse_lazy('item_servico:list')
