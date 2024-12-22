from django.urls import path
from . import views

app_name = 'crop_management'

urlpatterns = [
    path('', views.crop_list, name='crop_list'),
    path('create/', views.crop_create, name='crop_create'),
    path('<int:pk>/', views.crop_detail, name='crop_detail'),
    path('<int:pk>/update/', views.crop_update, name='crop_update'),
    path('<int:pk>/delete/', views.crop_delete, name='crop_delete'),
    path('schedule/', views.planting_schedule, name='planting_schedule'),
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('diseases/', views.disease_tracking, name='disease_tracking'),
]
