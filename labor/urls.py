from django.urls import path

from . import views

app_name = 'labor'

urlpatterns = [
    path('', views.WorkerListView.as_view(), name='worker_list'),
    path('add/', views.WorkerCreateView.as_view(), name='worker_create'),
    path('<int:pk>/edit/', views.WorkerUpdateView.as_view(), name='worker_update'),
    path('<int:pk>/delete/', views.WorkerDeleteView.as_view(), name='worker_delete'),
    path('tasks/', views.TaskListView.as_view(), name='task_list'),
    path('tasks/add/', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
]
