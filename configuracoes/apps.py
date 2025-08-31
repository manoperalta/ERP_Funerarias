from django.apps import AppConfig


class ConfiguracoesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'configuracoes'
    verbose_name = 'Configurações'
    
    def ready(self):
        """Importa signals quando o app estiver pronto."""
        import configuracoes.signals
