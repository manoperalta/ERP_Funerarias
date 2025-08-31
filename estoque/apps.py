from django.apps import AppConfig


class EstoqueConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'estoque'
    verbose_name = 'Estoque'
    
    def ready(self):
        """Importa signals quando o app estiver pronto."""
        import estoque.signals
