from django.urls import path
from rentals.views.buildings import (
    BuildingListView, BuildingDetailView,
    BuildingCreateView, BuildingUpdateView, BuildingDeleteView
)

urlpatterns = [
    path('', BuildingListView.as_view(), name='buildings_list'),
    path('<int:pk>/', BuildingDetailView.as_view(), name='buildings_detail'),
    path('create/', BuildingCreateView.as_view(), name='buildings_create'),
    path('<int:pk>/update/', BuildingUpdateView.as_view(), name='buildings_update'),
    path('<int:pk>/delete/', BuildingDeleteView.as_view(), name='buildings_delete'),
]
