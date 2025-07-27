import sys
from django.apps import AppConfig

class CartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart'

    def ready(self):
        if 'runserver' in sys.argv or 'gunicorn' in sys.argv:
            import cart.signals

