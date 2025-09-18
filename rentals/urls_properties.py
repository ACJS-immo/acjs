from django.urls import path
from rentals.views.properties import (
    PropertyListView, PropertyDetailView,
    PropertyCreateView, PropertyUpdateView, PropertyDeleteView
)

app_name = 'properties'
urlpatterns = [
    path('', PropertyListView.as_view(), name='list'),
    path('<int:pk>/', PropertyDetailView.as_view(), name='detail'),
    path('create/', PropertyCreateView.as_view(), name='create'),
    path('<int:pk>/update/', PropertyUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', PropertyDeleteView.as_view(), name='delete'),
]
