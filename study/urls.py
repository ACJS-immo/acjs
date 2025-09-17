from django.urls import path
from .views import RealEstatePropertyCreateView, RealEstatePropertyDetailView

urlpatterns = [
    path('add/', RealEstatePropertyCreateView.as_view(), name='add_property'),
    path('<int:pk>/', RealEstatePropertyDetailView.as_view(), name='property_detail'),
]
