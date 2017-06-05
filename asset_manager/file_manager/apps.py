from django.apps import AppConfig


class FileManagerConfig(AppConfig):
    name = 'file_manager'

    def ready(self):
        import file_manager.signals
