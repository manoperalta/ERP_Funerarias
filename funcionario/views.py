from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Funcionario
from .forms import FuncionarioForm, FuncionarioUsuarioForm
from .utils import criar_conta_funcionario, resetar_senha_funcionario, desativar_conta_funcionario, ativar_conta_funcionario
from app.mixins import LoginRequiredMixin, AdminDeleteMixin


class FuncionarioListView(LoginRequiredMixin, ListView):
    """View para listar funcionários."""
    model = Funcionario
    template_name = 'funcionario/funcionario_list.html'
    context_object_name = 'funcionarios'
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adicionar estatísticas de contas
        from .utils import estatisticas_contas_funcionarios
        context['stats'] = estatisticas_contas_funcionarios()
        return context


class FuncionarioDetailView(LoginRequiredMixin, DetailView):
    """View para exibir detalhes de um funcionário."""
    model = Funcionario
    template_name = 'funcionario/funcionario_detail.html'
    context_object_name = 'funcionario'


class FuncionarioCreateView(LoginRequiredMixin, CreateView):
    """View para criar um novo funcionário com conta de usuário."""
    model = Funcionario
    form_class = FuncionarioUsuarioForm
    template_name = 'funcionario/funcionario_create_form.html'
    success_url = reverse_lazy('funcionario:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Novo Funcionário'
        context['subtitle'] = 'Criar funcionário com conta de acesso'
        return context
    
    def form_valid(self, form):
        try:
            # O método save do formulário já cria o funcionário e o usuário
            funcionario = form.save()
            
            messages.success(
                self.request,
                f'Funcionário {funcionario.nome} criado com sucesso! '
                f'Login: {funcionario.usuario.username} | '
                f'Senha: (conforme definida no formulário)'
            )
            
            return redirect(self.success_url)
            
        except Exception as e:
            messages.error(
                self.request,
                f'Erro ao criar funcionário: {str(e)}'
            )
            return self.form_invalid(form)


class FuncionarioUpdateView(LoginRequiredMixin, UpdateView):
    """View para atualizar um funcionário."""
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'funcionario/funcionario_form.html'
    success_url = reverse_lazy('funcionario:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Funcionário'
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Sincronizar dados com conta de usuário
        if self.object.usuario:
            from .utils import sincronizar_dados_funcionario
            sincronizar_dados_funcionario(self.object)
            messages.success(
                self.request,
                f'Funcionário {self.object.nome} atualizado com sucesso!'
            )
        
        return response


class FuncionarioDeleteView(AdminDeleteMixin, DeleteView):
    """View para excluir um funcionário. Restrito a administradores."""
    model = Funcionario
    template_name = 'funcionario/funcionario_confirm_delete.html'
    success_url = reverse_lazy('funcionario:list')
    context_object_name = 'funcionario'


@login_required
@require_POST
def criar_conta_view(request, pk):
    """View para criar conta de login para um funcionário."""
    funcionario = get_object_or_404(Funcionario, pk=pk)
    
    if funcionario.usuario:
        messages.warning(request, f'{funcionario.nome} já possui conta de login.')
        return redirect('funcionario:detail', pk=pk)
    
    usuario, senha = criar_conta_funcionario(funcionario)
    
    if usuario:
        messages.success(
            request,
            f'Conta criada com sucesso para {funcionario.nome}! '
            f'Login: {usuario.username} | Senha: {senha}'
        )
    else:
        messages.error(request, f'Erro ao criar conta para {funcionario.nome}.')
    
    return redirect('funcionario:detail', pk=pk)


@login_required
@require_POST
def resetar_senha_view(request, pk):
    """View para resetar senha de um funcionário."""
    funcionario = get_object_or_404(Funcionario, pk=pk)
    
    if not funcionario.usuario:
        messages.warning(request, f'{funcionario.nome} não possui conta de login.')
        return redirect('funcionario:detail', pk=pk)
    
    nova_senha = resetar_senha_funcionario(funcionario)
    
    if nova_senha:
        messages.success(
            request,
            f'Senha resetada para {funcionario.nome}! '
            f'Nova senha: {nova_senha}'
        )
    else:
        messages.error(request, f'Erro ao resetar senha para {funcionario.nome}.')
    
    return redirect('funcionario:detail', pk=pk)


@login_required
@require_POST
def toggle_ativo_view(request, pk):
    """View para ativar/desativar conta de um funcionário."""
    funcionario = get_object_or_404(Funcionario, pk=pk)
    
    if not funcionario.usuario:
        messages.warning(request, f'{funcionario.nome} não possui conta de login.')
        return redirect('funcionario:detail', pk=pk)
    
    if funcionario.ativo:
        desativar_conta_funcionario(funcionario)
        messages.success(request, f'Conta de {funcionario.nome} desativada.')
    else:
        ativar_conta_funcionario(funcionario)
        messages.success(request, f'Conta de {funcionario.nome} ativada.')
    
    return redirect('funcionario:detail', pk=pk)
