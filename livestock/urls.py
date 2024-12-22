from django.urls import path
from . import views
from .views import (
    HealthRecordListView, HealthRecordCreateView, HealthRecordUpdateView, HealthRecordDeleteView,
    ProductionRecordListView, ProductionRecordCreateView, ProductionRecordUpdateView, ProductionRecordDeleteView,
    BreedingRecordListView, BreedingRecordCreateView, BreedingRecordUpdateView, BreedingRecordDeleteView
)

app_name = 'livestock'

urlpatterns = [
    # Animal URLs
    path('animals/', views.animal_list, name='animal_list'),
    path('animals/create/', views.animal_create, name='animal_create'),
    path('animals/<int:pk>/', views.animal_detail, name='animal_detail'),
    path('animals/<int:pk>/update/', views.animal_update, name='animal_update'),
    path('animals/<int:pk>/delete/', views.animal_delete, name='animal_delete'),
    
    # Health Record URLs
    path('health/', HealthRecordListView.as_view(), name='health_record_list'),
    path('health/add/', HealthRecordCreateView.as_view(), name='add_health_record'),
    path('health/<int:pk>/edit/', HealthRecordUpdateView.as_view(), name='edit_health_record'),
    path('health/<int:pk>/delete/', HealthRecordDeleteView.as_view(), name='delete_health_record'),

    # Production Record URLs
    path('production/', ProductionRecordListView.as_view(), name='production_record_list'),
    path('production/add/', ProductionRecordCreateView.as_view(), name='add_production_record'),
    path('production/<int:pk>/edit/', ProductionRecordUpdateView.as_view(), name='edit_production_record'),
    path('production/<int:pk>/delete/', ProductionRecordDeleteView.as_view(), name='delete_production_record'),

    # Breeding Record URLs
    path('breeding/', BreedingRecordListView.as_view(), name='breeding_record_list'),
    path('breeding/add/', BreedingRecordCreateView.as_view(), name='add_breeding_record'),
    path('breeding/<int:pk>/edit/', BreedingRecordUpdateView.as_view(), name='edit_breeding_record'),
    path('breeding/<int:pk>/delete/', BreedingRecordDeleteView.as_view(), name='delete_breeding_record'),
]
