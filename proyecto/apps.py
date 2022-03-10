from django.apps import AppConfig


class ProyectoConfig(AppConfig):
    name = 'proyecto'

    def ready(self):
        import proyecto.signals
