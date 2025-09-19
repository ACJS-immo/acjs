from django.urls import path
from rentals.views.tenants import (
    TenantListView, TenantDetailView,
    TenantCreateView, TenantUpdateView, TenantDeleteView
)

urlpatterns = [
    path('', TenantListView.as_view(), name='tenants_list'),
    path('<int:pk>/', TenantDetailView.as_view(), name='tenants_detail'),
    path('create/', TenantCreateView.as_view(), name='tenants_create'),
    path('<int:pk>/update/', TenantUpdateView.as_view(), name='tenants_update'),
    path('<int:pk>/delete/', TenantDeleteView.as_view(), name='tenants_delete'),
]
