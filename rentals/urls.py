from django.urls import path, include

app_name = 'rentals'
urlpatterns = [
    path('owners/', include('rentals.urls_owners')),
    path('buildings/', include('rentals.urls_buildings')),
    path('properties/', include('rentals.urls_properties')),
    path('tenants/', include('rentals.urls_tenants')),
    path('leases/', include('rentals.urls_leases')),
]
