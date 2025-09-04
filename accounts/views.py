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
    from item_servico.models import ItemServico
    from agendamento.models import Agendamento
    from financeiro.models import Financeiro
    from servico_contratado.models import ServicoContratado
    from datetime import datetime, timedelta
    from django.urls import reverse
    from django.db.models import Q, Sum
    
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
                    'url': reverse('pessoa_falecida:detail', kwargs={'pk': falecido.pk}),
                    'imagem_url': falecido.imagem.url if falecido.imagem else None
                })
        
        elif search_type == 'funcionario':
            funcionarios = Funcionario.objects.filter(
                Q(nome__icontains=search_query) |
                Q(telefone__icontains=search_query)
            )[:10]
            for funcionario in funcionarios:
                search_results.append({
                    'name': funcionario.nome,
                    'type': 'Funcionário',
                    'description': f'Cargo: {funcionario.cargo} | Telefone: {funcionario.telefone}',
                    'url': reverse('funcionario:detail', kwargs={'pk': funcionario.pk}),
                    'imagem_url': funcionario.usuario.foto_perfil.url if funcionario.usuario and funcionario.usuario.foto_perfil else None
                })
    
    # Estatísticas para administradores
    total_funcionarios = Funcionario.objects.count()
    total_familias = Familia.objects.count()
    total_falecidos = PessoaFalecida.objects.count()
    total_itens = ItemServico.objects.count()
    total_agendamentos = Agendamento.objects.count()
    
    # Receitas do mês atual
    hoje = datetime.now()
    inicio_mes = hoje.replace(day=1)
    receitas_mes = Financeiro.objects.filter(
        tipo='receita',
        status='pago',
        data_pagamento__gte=inicio_mes
    ).aggregate(total=Sum('valor'))['total'] or 0
    
    # Serviços contratados no mês
    servicos_mes = ServicoContratado.objects.filter(
        data_contratacao__gte=inicio_mes
    ).count()
    
    # Próximos agendamentos (próximos 7 dias)
    proxima_semana = hoje.date() + timedelta(days=7)
    agendamentos_proximos = Agendamento.objects.filter(
        data_agendamento__range=[hoje.date(), proxima_semana]
    ).order_by('data_agendamento', 'hora_agendamento')[:5]

    # Funcionários recentes
    funcionarios_recentes = Funcionario.objects.all().order_by('-id')[:4]
    
    context = {
        'user': request.user,
        'permissions': request.user.get_dashboard_permissions(),
        'dashboard_type': 'admin',
        'total_funcionarios': total_funcionarios,
        'total_familias': total_familias,
        'total_falecidos': total_falecidos,
        'total_itens': total_itens,
        'total_agendamentos': total_agendamentos,
        'receitas_mes': receitas_mes,
        'servicos_mes': servicos_mes,
        'agendamentos_proximos': agendamentos_proximos,
        'funcionarios_recentes': funcionarios_recentes,
        'search_results': search_results,
        'search_query': search_query,
        'search_type': search_type,
    }
    return render(request, 'accounts/dashboard_admin.html', context)


@login_required
def dashboard_vendedor(request):
    """Dashboard para vendedores."""
    from familia.models import Familia
    from pessoa_falecida.models import PessoaFalecida
    from item_servico.models import ItemServico
    from agendamento.models import Agendamento
    from financeiro.models import Financeiro
    from servico_contratado.models import ServicoContratado
    from datetime import datetime, timedelta
    from django.db.models import Sum, Count
    
    # Estatísticas para vendedores
    total_familias = Familia.objects.count()
    total_falecidos = PessoaFalecida.objects.count()
    total_itens = ItemServico.objects.count()
    total_agendamentos = Agendamento.objects.count()
    
    # Receitas do mês atual
    hoje = datetime.now()
    inicio_mes = hoje.replace(day=1)
    receitas_mes = Financeiro.objects.filter(
        tipo='receita',
        status='pago',
        data_pagamento__gte=inicio_mes
    ).aggregate(total=Sum('valor'))['total'] or 0
    
    # Serviços contratados no mês
    servicos_mes = ServicoContratado.objects.filter(
        data_contratacao__gte=inicio_mes
    ).count()
    
    # Próximos agendamentos (próximos 7 dias)
    proxima_semana = hoje.date() + timedelta(days=7)
    agendamentos_proximos = Agendamento.objects.filter(
        data_agendamento__range=[hoje.date(), proxima_semana]
    ).order_by('data_agendamento', 'hora_agendamento')[:5]

    itens_servico = ItemServico.objects.all()[:5]
    
    context = {
        'user': request.user,
        'permissions': request.user.get_dashboard_permissions(),
        'dashboard_type': 'vendedor',
        'total_familias': total_familias,
        'total_falecidos': total_falecidos,
        'total_itens': total_itens,
        'total_agendamentos': total_agendamentos,
        'receitas_mes': receitas_mes,
        'servicos_mes': servicos_mes,
        'agendamentos_proximos': agendamentos_proximos,
        'itens_servico': itens_servico,
    }
    return render(request, 'accounts/dashboard_vendedor.html', context)


@login_required
def dashboard_funcionario(request):
    """Dashboard para funcionários operacionais - Sistema To-Do List."""
    from agendamento.models import Agendamento
    from servico_contratado.models import ServicoContratado
    from pessoa_falecida.models import PessoaFalecida
    from funcionario.models import Funcionario
    from financeiro.models import Financeiro
    from datetime import datetime, timedelta
    from django.db.models import Sum, Count
    
    hoje = datetime.now().date()
    proximos_7_dias = hoje + timedelta(days=7)
    
    # Estatísticas gerais para funcionários
    total_funcionarios = Funcionario.objects.count()
    total_agendamentos = Agendamento.objects.count()
    
    # Agendamentos pendentes (próximos 7 dias)
    agendamentos_pendentes = Agendamento.objects.filter(
        data_agendamento__range=[hoje, proximos_7_dias]
    ).count()
    
    # Tarefas concluídas no mês (usando serviços contratados como proxy)
    inicio_mes = datetime.now().replace(day=1)
    tarefas_concluidas = ServicoContratado.objects.filter(
        data_contratacao__gte=inicio_mes
    ).count()
    
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
        ).prefetch_related('itens__item_servico')
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
        'total_funcionarios': total_funcionarios,
        'total_agendamentos': total_agendamentos,
        'agendamentos_pendentes': agendamentos_pendentes,
        'tarefas_concluidas': tarefas_concluidas,
        'todo_cards': todo_cards,
        'total_sepultamentos': total_sepultamentos,
        'sepultamentos_hoje': sepultamentos_hoje,
        'sepultamentos_urgentes': sepultamentos_urgentes,
    }
    return render(request, 'accounts/dashboard_funcionario_todo.html', context)
