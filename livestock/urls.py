from django.urls import path
from . import views

app_name = 'livestock'

urlpatterns = [
    # Animal URLs
    path('', views.animal_list, name='animal_list'),
    path('create/', views.animal_create, name='animal_create'),
    path('<int:pk>/', views.animal_detail, name='animal_detail'),
    path('<int:pk>/update/', views.animal_update, name='animal_update'),
    path('<int:pk>/delete/', views.animal_delete, name='animal_delete'),
    
    # Health Record URLs
    path('health/', views.health_record_list, name='health_record_list'),
    path('<int:animal_pk>/health/create/', views.health_record_create, name='health_record_create'),
    
    # Production Record URLs
    path('production/', views.production_record_list, name='production_record_list'),
    path('<int:animal_pk>/production/create/', views.production_record_create, name='production_record_create'),
    
    # Breeding Record URLs
    path('breeding/', views.breeding_record_list, name='breeding_record_list'),
    path('breeding/create/', views.breeding_record_create, name='breeding_record_create'),
]
