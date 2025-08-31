from django.db.models.signals import post_save, post_delete
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


@receiver(post_save, sender=User)
def log_criacao_usuario(sender, instance, created, **kwargs):
    """Registra log da criação de usuários."""
    if created:
        print(f"[LOG USER] Novo usuário criado: {instance.username} - Cargo: {instance.cargo}")


@receiver(post_save, sender=User)
def validar_permissoes_usuario(sender, instance, created, **kwargs):
    """Valida e ajusta permissões baseadas no cargo."""
    if instance.cargo == 'adm':
        # Administradores têm acesso total
        instance.is_staff = True
        if not created:  # Evita loop infinito
            instance.save(update_fields=['is_staff'])
    elif instance.cargo in ['florista', 'coveiro', 'preparador']:
        # Funcionários operacionais não têm acesso admin
        if instance.is_staff:
            instance.is_staff = False
            if not created:
                instance.save(update_fields=['is_staff'])


@receiver(user_logged_in)
def log_login_usuario(sender, request, user, **kwargs):
    """Registra log de login dos usuários."""
    ip_address = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
    
    print(f"[LOG LOGIN] {user.username} ({user.cargo}) - IP: {ip_address} - {timezone.now()}")
    
    # Aqui poderia salvar em modelo de auditoria
    # AuditoriaLogin.objects.create(
    #     usuario=user,
    #     ip_address=ip_address,
    #     user_agent=user_agent,
    #     data_login=timezone.now()
    # )


@receiver(user_logged_out)
def log_logout_usuario(sender, request, user, **kwargs):
    """Registra log de logout dos usuários."""
    if user:
        print(f"[LOG LOGOUT] {user.username} - {timezone.now()}")


@receiver(post_delete, sender=User)
def log_exclusao_usuario(sender, instance, **kwargs):
    """Registra log da exclusão de usuários."""
    print(f"[LOG USER] Usuário excluído: {instance.username} - Cargo: {instance.cargo}")


def get_client_ip(request):
    """Obtém IP real do cliente considerando proxies."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Signal personalizado para notificações
from django.dispatch import Signal

# Cria signal personalizado para notificações
notificacao_sistema = Signal()


@receiver(notificacao_sistema)
def processar_notificacao(sender, tipo, mensagem, usuario=None, **kwargs):
    """Processa notificações do sistema."""
    print(f"[NOTIFICAÇÃO] {tipo.upper()}: {mensagem}")
    
    # Aqui poderia implementar:
    # - Envio de email
    # - Notificação push
    # - Integração com Slack/Discord
    # - Armazenamento em banco de dados
    
    if usuario:
        print(f"[NOTIFICAÇÃO] Destinatário: {usuario.username}")


# Exemplo de uso do signal personalizado:
# from accounts.signals import notificacao_sistema
# notificacao_sistema.send(
#     sender=None,
#     tipo='estoque_baixo',
#     mensagem='Produto X está com estoque baixo',
#     usuario=admin_user
# )

