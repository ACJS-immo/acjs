from django.apps import AppConfig

class RentalsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rentals'

    # def ready(self):
    #     # Importe les signaux si tu en as
    #     import rentals.signals
