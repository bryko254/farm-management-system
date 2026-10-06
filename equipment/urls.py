from django.urls import path

from . import views

app_name = 'equipment'

urlpatterns = [
    path('', views.EquipmentListView.as_view(), name='equipment_list'),
    path('add/', views.EquipmentCreateView.as_view(), name='equipment_create'),
    path('<int:pk>/edit/', views.EquipmentUpdateView.as_view(), name='equipment_update'),
    path('<int:pk>/delete/', views.EquipmentDeleteView.as_view(), name='equipment_delete'),
    path('maintenance/', views.MaintenanceScheduleView.as_view(), name='maintenance_schedule'),
]
