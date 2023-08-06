from django.apps import AppConfig


class KeenDashboardConfig(AppConfig):
    name = 'keen_dashboard'

    def ready(self):
        super().ready()

