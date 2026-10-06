from django.urls import path

from . import views

app_name = 'livestock'

urlpatterns = [
    path('animals/', views.animal_list, name='animal_list'),
    path('animals/create/', views.animal_create, name='animal_create'),
    path('animals/<int:pk>/', views.animal_detail, name='animal_detail'),
    path('animals/<int:pk>/update/', views.animal_update, name='animal_update'),
    path('animals/<int:pk>/delete/', views.animal_delete, name='animal_delete'),

    path('health/', views.HealthRecordListView.as_view(), name='health_record_list'),
    path('health/add/', views.HealthRecordCreateView.as_view(), name='add_health_record'),
    path('health/<int:pk>/edit/', views.HealthRecordUpdateView.as_view(), name='edit_health_record'),
    path('health/<int:pk>/delete/', views.HealthRecordDeleteView.as_view(), name='delete_health_record'),

    path('production/', views.ProductionRecordListView.as_view(), name='production_record_list'),
    path('production/add/', views.ProductionRecordCreateView.as_view(), name='add_production_record'),
    path('production/<int:pk>/edit/', views.ProductionRecordUpdateView.as_view(), name='edit_production_record'),
    path('production/<int:pk>/delete/', views.ProductionRecordDeleteView.as_view(), name='delete_production_record'),

    path('breeding/', views.BreedingRecordListView.as_view(), name='breeding_record_list'),
    path('breeding/add/', views.BreedingRecordCreateView.as_view(), name='add_breeding_record'),
    path('breeding/<int:pk>/edit/', views.BreedingRecordUpdateView.as_view(), name='edit_breeding_record'),
    path('breeding/<int:pk>/delete/', views.BreedingRecordDeleteView.as_view(), name='delete_breeding_record'),
]
