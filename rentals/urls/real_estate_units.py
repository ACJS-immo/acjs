from django.urls import path
from rentals.views.real_estate_units import (
    RealEstateUnitListView, RealEstateUnitDetailView,
    RealEstateUnitCreateView, RealEstateUnitUpdateView, RealEstateUnitDeleteView
)

urlpatterns = [
    path('', RealEstateUnitListView.as_view(), name='real_estate_unit_list'),
    path('<int:pk>/', RealEstateUnitDetailView.as_view(), name='real_estate_unit_detail'),
    path('create/', RealEstateUnitCreateView.as_view(), name='real_estate_unit_create'),
    path('<int:pk>/update/', RealEstateUnitUpdateView.as_view(), name='real_estate_unit_update'),
    path('<int:pk>/delete/', RealEstateUnitDeleteView.as_view(), name='real_estate_unit_delete'),
]
