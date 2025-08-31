from django.apps import AppConfig


class DocumentosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'documentos'
    verbose_name = 'Documentos'
    
    def ready(self):
        """Importa signals quando o app estiver pronto."""
        import documentos.signals
