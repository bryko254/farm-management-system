from django.urls import path
from . import views

app_name = 'compliance'

urlpatterns = [
    path('', views.compliance_dashboard, name='compliance_dashboard'),
    path('certifications/', views.certification_list, name='certification_list'),
    path('documents/', views.document_list, name='document_list'),
    path('food-safety/', views.food_safety_records, name='food_safety_records'),
    path('environmental/', views.environmental_compliance, name='environmental_compliance'),
]
