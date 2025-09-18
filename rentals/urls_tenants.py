from django.urls import path
from rentals.views.tenants import (
    TenantListView, TenantDetailView,
    TenantCreateView, TenantUpdateView, TenantDeleteView
)

app_name = 'tenants'
urlpatterns = [
    path('', TenantListView.as_view(), name='list'),
    path('<int:pk>/', TenantDetailView.as_view(), name='detail'),
    path('create/', TenantCreateView.as_view(), name='create'),
    path('<int:pk>/update/', TenantUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', TenantDeleteView.as_view(), name='delete'),
]
