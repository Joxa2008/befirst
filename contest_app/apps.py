from django.apps import AppConfig


class ContestAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contest_app'

    def ready(self):
        import contest_app.signals