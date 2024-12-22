from django.urls import path
from . import views

app_name = 'labor'

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('<int:pk>/', views.employee_detail, name='employee_detail'),
    path('create/', views.employee_create, name='employee_create'),
    path('schedules/', views.work_schedules, name='work_schedules'),
    path('tasks/', views.task_management, name='task_management'),
    path('performance/', views.performance_tracking, name='performance_tracking'),
]
