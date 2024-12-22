from django.urls import path
from . import views

app_name = 'land_management'

urlpatterns = [
    path('', views.field_list, name='field_list'),
    path('field/<int:pk>/', views.field_detail, name='field_detail'),
    path('field/create/', views.field_create, name='field_create'),
    path('field/<int:pk>/update/', views.field_update, name='field_update'),
    path('field/<int:pk>/delete/', views.field_delete, name='field_delete'),
    path('soil-analysis/', views.soil_analysis_list, name='soil_analysis_list'),
    path('field/<int:field_pk>/soil-analysis/create/', views.soil_analysis_create, name='soil_analysis_create'),
    path('irrigation/', views.irrigation_list, name='irrigation_list'),
    path('field/<int:field_pk>/irrigation/create/', views.irrigation_create, name='irrigation_create'),
    path('irrigation/<int:system_pk>/schedule/create/', views.irrigation_schedule_create, name='irrigation_schedule_create'),
]
