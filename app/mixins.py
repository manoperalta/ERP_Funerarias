from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import redirect


class AdminRequiredMixin(UserPassesTestMixin):
    """
    Mixin que restringe acesso apenas a usuários administradores.
    """
    
    def test_func(self):
        """Testa se o usuário é administrador."""
        return self.request.user.is_authenticated and self.request.user.is_admin
    
    def handle_no_permission(self):
        """Trata quando o usuário não tem permissão."""
        if self.request.user.is_authenticated:
            messages.error(
                self.request, 
                'Você não tem permissão para realizar esta ação. Apenas administradores podem excluir registros.'
            )
            # Redireciona para a lista do modelo atual
            if hasattr(self, 'model'):
                app_label = self.model._meta.app_label
                model_name = self.model._meta.model_name
                try:
                    from django.urls import reverse
                    list_url = reverse(f'{app_label}:list')
                    return redirect(list_url)
                except:
                    pass
            return redirect('accounts:dashboard')
        else:
            return super().handle_no_permission()


class AdminDeleteMixin(LoginRequiredMixin, AdminRequiredMixin):
    """
    Mixin que combina autenticação obrigatória com restrição de exclusão para administradores.
    """
    pass


class LoginRequiredMixin(LoginRequiredMixin):
    """
    Mixin personalizado que herda do LoginRequiredMixin do Django
    para garantir consistência nas configurações de login.
    """
    pass

