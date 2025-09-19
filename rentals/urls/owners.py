from django.urls import path
from rentals.views.owners import (
    OwnerListView, OwnerDetailView,
    OwnerCreateView, OwnerUpdateView, OwnerDeleteView
)

urlpatterns = [
    path('', OwnerListView.as_view(), name='owners_list'),
    path('<int:pk>/', OwnerDetailView.as_view(), name='owners_detail'),
    path('create/', OwnerCreateView.as_view(), name='owners_create'),
    path('<int:pk>/update/', OwnerUpdateView.as_view(), name='owners_update'),
    path('<int:pk>/delete/', OwnerDeleteView.as_view(), name='owners_delete'),
]
