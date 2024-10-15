from django.apps import AppConfig
from .signals import *

class SlackAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'slack_app'

    def ready(self):
        from django.db.models.signals import post_migrate
        post_migrate.connect(my_callback, sender=self)

