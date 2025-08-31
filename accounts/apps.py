from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = 'Contas de Usuário'
    
    def ready(self):
        """Importa signals quando o app estiver pronto."""
        import accounts.signals
