from django.apps import AppConfig


class JournalConfig(AppConfig):
    name = 'journal'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import journal.signals

