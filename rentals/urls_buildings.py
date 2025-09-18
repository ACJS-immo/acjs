from django.urls import path
from rentals.views.buildings import (
    BuildingListView, BuildingDetailView,
    BuildingCreateView, BuildingUpdateView, BuildingDeleteView
)

app_name = 'buildings'
urlpatterns = [
    path('', BuildingListView.as_view(), name='list'),
    path('<int:pk>/', BuildingDetailView.as_view(), name='detail'),
    path('create/', BuildingCreateView.as_view(), name='create'),
    path('<int:pk>/update/', BuildingUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', BuildingDeleteView.as_view(), name='delete'),
]
