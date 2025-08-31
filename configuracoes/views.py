from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import ConfiguracaoFuneraria
from .forms import ConfiguracaoFunerariaForm


def is_admin(user):
    """Verifica se o usuário é administrador."""
    return user.is_authenticated and hasattr(user, 'cargo') and user.cargo == 'adm'


@login_required
@user_passes_test(is_admin)
def configuracoes_view(request):
    """View para visualizar as configurações da funerária."""
    configuracao = ConfiguracaoFuneraria.get_configuracao_ativa()
    
    context = {
        'configuracao': configuracao,
        'user': request.user,
    }
    return render(request, 'configuracoes/configuracoes_detail.html', context)


class ConfiguracaoFunerariaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View para editar configurações da funerária."""
    model = ConfiguracaoFuneraria
    form_class = ConfiguracaoFunerariaForm
    template_name = 'configuracoes/configuracoes_form.html'
    success_url = reverse_lazy('configuracoes:detail')
    
    def test_func(self):
        """Verifica se o usuário tem permissão para editar configurações."""
        return is_admin(self.request.user)
    
    def get_object(self):
        """Retorna a configuração ativa."""
        return ConfiguracaoFuneraria.get_configuracao_ativa()
    
    def form_valid(self, form):
        """Processa o formulário válido."""
        response = super().form_valid(form)
        messages.success(
            self.request, 
            'Configurações da funerária atualizadas com sucesso!'
        )
        return response
    
    def get_context_data(self, **kwargs):
        """Adiciona dados extras ao contexto."""
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


@login_required
def configuracoes_preview(request):
    """Preview das configurações aplicadas ao sistema."""
    configuracao = ConfiguracaoFuneraria.get_configuracao_ativa()
    
    context = {
        'configuracao': configuracao,
        'user': request.user,
        'preview_mode': True,
    }
    return render(request, 'configuracoes/configuracoes_preview.html', context)
