from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('healthz/', views.healthz, name='healthz'),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('land/', include('land_management.urls')),
    path('crops/', include('crop_management.urls')),
    path('livestock/', include('livestock.urls')),
    path('equipment/', include('equipment.urls')),
    path('labor/', include('labor.urls')),
    path('finance/', include('finance.urls')),
    path('compliance/', include('compliance.urls')),
]
