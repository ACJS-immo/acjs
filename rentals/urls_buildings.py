from django.urls import path
from . import views

app_name = 'buildings'
urlpatterns = [
    path('', views.BuildingListView.as_view(), name='list'),
    path('<int:pk>/', views.BuildingDetailView.as_view(), name='detail'),
    path('create/', views.BuildingCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.BuildingUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.BuildingDeleteView.as_view(), name='delete'),
]
