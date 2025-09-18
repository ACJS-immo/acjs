from django.urls import path
from rentals.views.owners import (
    OwnerListView, OwnerDetailView,
    OwnerCreateView, OwnerUpdateView, OwnerDeleteView
)

app_name = 'owners'
urlpatterns = [
    path('', OwnerListView.as_view(), name='list'),
    path('<int:pk>/', OwnerDetailView.as_view(), name='detail'),
    path('create/', OwnerCreateView.as_view(), name='create'),
    path('<int:pk>/update/', OwnerUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', OwnerDeleteView.as_view(), name='delete'),
]
