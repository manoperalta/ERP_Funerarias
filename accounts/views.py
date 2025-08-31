from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomLoginView(LoginView):
    """View personalizada para login."""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        """Redireciona baseado no cargo do usuário."""
        user = self.request.user
        if user.is_admin:
            return reverse_lazy('dashboard_admin')
        elif user.is_vendedor:
            return reverse_lazy('dashboard_vendedor')
        elif user.is_funcionario_operacional:
            return reverse_lazy('dashboard_funcionario')
        else:
            return reverse_lazy('home')


class CustomLogoutView(LogoutView):
    """View personalizada para logout."""
    next_page = 'accounts:login'


class UserRegistrationView(CreateView):
    """View para registro de novos usuários."""
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        """Processa o formulário válido."""
        response = super().form_valid(form)
        messages.success(
            self.request, 
            'Usuário criado com sucesso! Faça login para continuar.'
        )
        return response


class UserProfileView(LoginRequiredMixin, UpdateView):
    """View para editar perfil do usuário."""
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        """Retorna o usuário atual."""
        return self.request.user
    
    def form_valid(self, form):
        """Processa o formulário válido."""
        response = super().form_valid(form)
        messages.success(self.request, 'Perfil atualizado com sucesso!')
        return response


@login_required
def dashboard_admin(request):
    """Dashboard para administradores."""
    context = {
        'user': request.user,
        'dashboard_type': 'admin',
        'total_funcionarios': 0,
        'total_familias': 0,
        'total_agendamentos': 0,
        'total_itens': 0,
        'receita_mensal': "0,00",
    }
    return render(request, 'accounts/dashboard_admin_working.html', context)


@login_required
def dashboard_vendedor(request):
    """Dashboard para vendedores."""
    from familia.models import Familia
    from pessoa_falecida.models import PessoaFalecida
    from item_servico.models import ItemServico
    from agendamento.models import Agendamento
    from datetime import datetime, timedelta
    
    # Estatísticas para vendedores
    total_familias = Familia.objects.count()
    total_falecidos = PessoaFalecida.objects.count()
    total_itens = ItemServico.objects.count()
    
    # Próximos agendamentos (próximos 7 dias)
    hoje = datetime.now().date()
    proxima_semana = hoje + timedelta(days=7)
    agendamentos_proximos = Agendamento.objects.filter(
        data_agendamento__range=[hoje, proxima_semana]
    ).order_by('data_agendamento', 'hora_agendamento')[:5]
    
    context = {
        'user': request.user,
        'permissions': request.user.get_dashboard_permissions(),
        'dashboard_type': 'vendedor',
        'total_familias': total_familias,
        'total_falecidos': total_falecidos,
        'total_itens': total_itens,
        'agendamentos_proximos': agendamentos_proximos,
    }
    return render(request, 'accounts/dashboard_vendedor.html', context)


@login_required
def dashboard_funcionario(request):
    """Dashboard para funcionários operacionais."""
    from agendamento.models import Agendamento
    from datetime import datetime, timedelta
    
    # Busca apenas os agendamentos do usuário atual
    hoje = datetime.now().date()
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    fim_semana = inicio_semana + timedelta(days=6)
    
    # Agendamentos do funcionário
    agendamentos = Agendamento.objects.filter(
        funcionario_responsavel=request.user
    ).order_by('data_agendamento', 'hora_agendamento')[:10]
    
    # Estatísticas
    agendamentos_hoje = agendamentos.filter(data_agendamento=hoje)
    agendamentos_semana = agendamentos.filter(
        data_agendamento__range=[inicio_semana, fim_semana]
    )
    agendamentos_pendentes = agendamentos.filter(status='pendente')
    agendamentos_concluidos = agendamentos.filter(status='concluido')
    
    context = {
        'user': request.user,
        'permissions': request.user.get_dashboard_permissions(),
        'dashboard_type': 'funcionario',
        'agendamentos': agendamentos,
        'agendamentos_hoje': agendamentos_hoje,
        'agendamentos_semana': agendamentos_semana,
        'agendamentos_pendentes': agendamentos_pendentes,
        'agendamentos_concluidos': agendamentos_concluidos,
        'cargo': request.user.get_cargo_display()
    }
    return render(request, 'accounts/dashboard_funcionario.html', context)
