# rentals/urls/home.py
from django.urls import path
from rentals.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # ✅ URL 'home' dans le sous-package
]