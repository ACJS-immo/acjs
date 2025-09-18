"""
URL configuration for acjs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
                  path("admin/", admin.site.urls),
                  path("study/", include("study.urls")),
                  path("owners/", include("rentals.urls_owners")),
                  path("buildings/", include("rentals.urls_buildings")),
                  path("properties/", include("rentals.urls_properties")),
                  path("tenants/", include("rentals.urls_tenants")),
                  path("leases/", include("rentals.urls_leases")),
                  path('i18n/', include('django.conf.urls.i18n')),
                  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
