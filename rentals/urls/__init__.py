# rentals/urls/__init__.py
from django.urls import path, include

# Importe les sous-modules d'URLs
from . import owners, buildings, properties, tenants, leases, home
from ..views.home import HomeView

app_name = 'rentals'
# Déclare urlpatterns ici pour que Django le trouve
urlpatterns = [
    path('', include(home.urlpatterns), name='home'),  # ✅ Ajoute l'URL 'home'
    path('owners/', include(owners.urlpatterns)),
    path('buildings/', include(buildings.urlpatterns)),
    path('properties/', include(properties.urlpatterns)),
    path('tenants/', include(tenants.urlpatterns)),
    path('leases/', include(leases.urlpatterns)),
    ]
