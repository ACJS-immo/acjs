from django.urls import path
from rentals.views.properties import (
    PropertyListView, PropertyDetailView,
    PropertyCreateView, PropertyUpdateView, PropertyDeleteView
)

urlpatterns = [
    path('', PropertyListView.as_view(), name='properties_list'),
    path('<int:pk>/', PropertyDetailView.as_view(), name='properties_detail'),
    path('create/', PropertyCreateView.as_view(), name='properties_create'),
    path('<int:pk>/update/', PropertyUpdateView.as_view(), name='properties_update'),
    path('<int:pk>/delete/', PropertyDeleteView.as_view(), name='properties_delete'),
]
