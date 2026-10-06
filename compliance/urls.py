from django.urls import path

from . import views

app_name = 'compliance'

urlpatterns = [
    path('', views.CertificationListView.as_view(), name='certification_list'),
    path('add/', views.CertificationCreateView.as_view(), name='certification_create'),
    path('<int:pk>/edit/', views.CertificationUpdateView.as_view(), name='certification_update'),
    path('<int:pk>/delete/', views.CertificationDeleteView.as_view(), name='certification_delete'),
]
