from django.urls import path
from . import views

app_name = 'equipment'

urlpatterns = [
    path('', views.equipment_list, name='equipment_list'),
    path('<int:pk>/', views.equipment_detail, name='equipment_detail'),
    path('create/', views.equipment_create, name='equipment_create'),
    path('maintenance/', views.maintenance_schedule, name='maintenance_schedule'),
    path('fuel-tracking/', views.fuel_tracking, name='fuel_tracking'),
]
