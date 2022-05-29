from django.apps import AppConfig


class RevisarDocumentosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'revisar_documentos'

    def ready(self):
        import revisar_documentos.signals
