from django.apps import AppConfig
from django.conf import settings


class ApiConfig(AppConfig):
    name = '{}.api'.format(settings.PROJECT)
