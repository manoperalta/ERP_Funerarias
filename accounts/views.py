from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


def home_redirect(request):
    """Redireciona usuários baseado no status de autenticação e cargo."""
    if request.user.is_authenticated:
        if request.user.is_admin:
            return redirect('dashboard_admin')
        elif request.user.is_vendedor:
            return redirect('dashboard_vendedor')
        elif request.user.is_funcionario_operacional:
            return redirect('dashboard_funcionario')
        else:
            return redirect('dashboard_admin')  # Fallback para admin
    else:
        return redirect('accounts:login')


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


def custom_logout_view(request):
    logout(request)
    return redirect(reverse_lazy('accounts:login'))


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
    from familia.models import Familia
    from pessoa_falecida.models import PessoaFalecida
    from funcionario.models import Funcionario
    from django.urls import reverse
    from django.db.models import Q
    
    # Funcionalidade de busca
    search_results = []
    search_query = request.GET.get('search_query', '')
    search_type = request.GET.get('search_type', 'familia')
    
    if search_query:
        if search_type == 'familia':
            familias = Familia.objects.filter(
                Q(nome_responsavel__icontains=search_query) |
                Q(telefone__icontains=search_query) |
                Q(email__icontains=search_query)
            )[:10]
            for familia in familias:
                search_results.append({
                    'name': familia.nome_responsavel,
                    'type': 'Família',
                    'description': f'Telefone: {familia.telefone} | Email: {familia.email}',
                    'url': reverse('familia:detail', kwargs={'pk': familia.pk})
                })
        
        elif search_type == 'falecido':
            falecidos = PessoaFalecida.objects.filter(
                Q(nome__icontains=search_query) |
                Q(documento_cpf_rg__icontains=search_query)
            )[:10]
            for falecido in falecidos:
                search_results.append({
                    'name': falecido.nome,
                    'type': 'Falecido',
                    'description': f'Família: {falecido.familia.nome_responsavel} | Data: {falecido.data_falecimento.strftime("%d/%m/%Y")}',
                    'url': reverse('pessoa_falecida:detail', kwargs={'pk': falecido.pk})
                })
        
        elif search_type == 'funcionario':
            funcionarios = Funcionario.objects.filter(
                Q(nome__icontains=search_query) |
                Q(cpf__icontains=search_query) |
                Q(telefone__icontains=search_query)
            )[:10]
            for funcionario in funcionarios:
                search_results.append({
                    'name': funcionario.nome,
                    'type': 'Funcionário',
                    'description': f'Cargo: {funcionario.cargo} | Telefone: {funcionario.telefone}',
                    'url': reverse('funcionario:detail', kwargs={'pk': funcionario.pk})
                })
    
    context = {
        'user': request.user,
        'dashboard_type': 'admin',
        'total_funcionarios': Funcionario.objects.count(),
        'total_familias': Familia.objects.count(),
        'total_agendamentos': 0,
        'total_itens': 0,
        'receita_mensal': "0,00",
        'search_results': search_results,
        'search_query': search_query,
        'search_type': search_type,
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
    """Dashboard para funcionários operacionais - Sistema To-Do List."""
    from agendamento.models import Agendamento
    from servico_contratado.models import ServicoContratado
    from pessoa_falecida.models import PessoaFalecida
    from datetime import datetime, timedelta
    
    hoje = datetime.now().date()
    proximos_7_dias = hoje + timedelta(days=7)
    
    # Buscar todos os sepultamentos próximos (não apenas do funcionário)
    # Funcionários operacionais trabalham em equipe nos sepultamentos
    agendamentos_proximos = Agendamento.objects.filter(
        data_sepultamento__date__range=[hoje, proximos_7_dias]
    ).select_related('pessoa_falecida').order_by('data_sepultamento')
    
    # Criar cards de to-do list organizados por sepultamento
    todo_cards = []
    
    for agendamento in agendamentos_proximos:
        # Buscar serviços contratados relacionados ao falecido
        servicos_contratados = ServicoContratado.objects.filter(
            pessoa_falecida=agendamento.pessoa_falecida
        ).select_related('item_servico')
        
        # Determinar tarefas específicas baseadas no cargo do usuário
        tarefas_usuario = []
        cargo = request.user.cargo
        
        if cargo == 'florista':
            tarefas_usuario = [
                'Preparar arranjos florais',
                'Decorar local do velório',
                'Organizar flores no caixão',
                'Preparar coroas de flores'
            ]
        elif cargo == 'preparador':
            tarefas_usuario = [
                'Preparar o corpo',
                'Vestir o falecido',
                'Aplicar maquiagem',
                'Posicionar no caixão'
            ]
        elif cargo == 'coveiro':
            tarefas_usuario = [
                'Preparar local do sepultamento',
                'Escavar sepultura',
                'Auxiliar no transporte',
                'Realizar sepultamento'
            ]
        
        # Calcular urgência baseada na proximidade da data
        dias_restantes = (agendamento.data_sepultamento.date() - hoje).days
        if dias_restantes == 0:
            urgencia = 'hoje'
        elif dias_restantes == 1:
            urgencia = 'amanha'
        elif dias_restantes <= 3:
            urgencia = 'urgente'
        else:
            urgencia = 'normal'
        
        card = {
            'agendamento': agendamento,
            'servicos_contratados': servicos_contratados,
            'tarefas_usuario': tarefas_usuario,
            'urgencia': urgencia,
            'dias_restantes': dias_restantes,
        }
        todo_cards.append(card)
    
    # Estatísticas para o dashboard
    total_sepultamentos = len(todo_cards)
    sepultamentos_hoje = len([c for c in todo_cards if c['urgencia'] == 'hoje'])
    sepultamentos_urgentes = len([c for c in todo_cards if c['urgencia'] in ['hoje', 'amanha', 'urgente']])
    
    context = {
        'user': request.user,
        'permissions': request.user.get_dashboard_permissions(),
        'dashboard_type': 'funcionario',
        'cargo': request.user.get_cargo_display(),
        'todo_cards': todo_cards,
        'total_sepultamentos': total_sepultamentos,
        'sepultamentos_hoje': sepultamentos_hoje,
        'sepultamentos_urgentes': sepultamentos_urgentes,
    }
    return render(request, 'accounts/dashboard_funcionario_todo.html', context)
