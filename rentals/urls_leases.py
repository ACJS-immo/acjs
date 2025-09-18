from django.urls import path
from rentals.views.leases import (
    LeaseListView, LeaseDetailView,
    LeaseCreateView, LeaseUpdateView, LeaseDeleteView
)

app_name = 'leases'
urlpatterns = [
    path('', LeaseListView.as_view(), name='list'),
    path('<int:pk>/', LeaseDetailView.as_view(), name='detail'),
    path('create/', LeaseCreateView.as_view(), name='create'),
    path('<int:pk>/update/', LeaseUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', LeaseDeleteView.as_view(), name='delete'),
]
