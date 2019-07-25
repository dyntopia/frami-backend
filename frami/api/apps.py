from django.apps import AppConfig
from django.conf import settings


class ApiConfig(AppConfig):
    name = '{}.api'.format(settings.PROJECT)

    def ready(self):
        from . import signals
        assert signals  # for pyflakes

        return super().ready()
