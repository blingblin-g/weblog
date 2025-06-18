from django.apps import AppConfig
import os


class WeblogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weblog'
    path = os.path.dirname(os.path.abspath(__file__)) 