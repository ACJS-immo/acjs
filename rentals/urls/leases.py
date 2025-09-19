from django.urls import path
from rentals.views.leases import (
    LeaseListView, LeaseDetailView,
    LeaseCreateView, LeaseUpdateView, LeaseDeleteView
)

urlpatterns = [
    path('', LeaseListView.as_view(), name='leases_list'),
    path('<int:pk>/', LeaseDetailView.as_view(), name='leases_detail'),
    path('create/', LeaseCreateView.as_view(), name='leases_create'),
    path('<int:pk>/update/', LeaseUpdateView.as_view(), name='leases_update'),
    path('<int:pk>/delete/', LeaseDeleteView.as_view(), name='leases_delete'),
]
